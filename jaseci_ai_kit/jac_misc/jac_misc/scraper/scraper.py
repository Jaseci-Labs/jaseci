from jaseci.jsorc.live_actions import jaseci_action
from playwright.sync_api import sync_playwright, Page
from typing import Union
from re import search
from copy import deepcopy


@jaseci_action(act_group=["wbs"], allow_remote=True)
def setup():
    pass


@jaseci_action(act_group=["wbs"], allow_remote=True)
def url_to_filename(url: str):
    return "".join(c for c in url if c.isalnum())


@jaseci_action(act_group=["wbs"], allow_remote=True)
def scrape(pages: list, pre_configs: list = [], detailed: bool = False):
    content = ""
    urls = {"scanned": set(), "scraped": set(), "crawled": set()}
    with sync_playwright() as spw:
        browser = spw.chromium.launch()
        page = browser.new_page()

        while pages:
            pg: dict = pages.pop(0)

            goto(page, pg.get("goto") or {}, urls)
            content += getters(page, pg.get("getters") or [], urls)
            crawler(page, pg.get("crawler") or {}, urls, pages, pre_configs)

        browser.close()

    content = " ".join(content.split())

    if detailed:
        return {
            "content": content,
            "scanned": list(urls["scanned"]),
            "scraped": list(urls["scraped"]),
        }

    return content


def goto(page: Page, specs: dict, urls: dict):
    if specs:
        post = get_script(specs, "post")
        run_scripts(page, get_script(specs, "pre"), urls)

        print(f'[goto]: loading {specs["url"]}')

        page.goto(**specs)
        add_url(page, urls)

        run_scripts(page, post, urls)


def getters(page: Page, specss: list[dict], urls: dict):
    content = ""
    for specs in specss:
        if specs:
            post = get_script(specs, "post")
            run_scripts(page, get_script(specs, "pre"), urls)

            exel_str = ""
            for exel in (
                specs.get("excluded_element", ["script", "style", "link", "noscript"])
                or []
            ):
                exel_str += (
                    f'clone.querySelectorAll("{exel}").forEach(d => d.remove());\n'
                )

            method = specs.get("method")
            if method == "selector":
                expression = f"""
                    Array.prototype.map.call(
                        document.querySelectorAll("{specs.get("expression")}"),
                        d => {{
                            clone = d.cloneNode(true);
                            {exel_str}
                            return clone.textContent;
                        }}).join("\n");
                """
            elif method == "custom":
                expression = f'{{{specs.get("expression")}}}'
            elif method == "none":
                expression = '""'
            else:
                expression = f"""{{
                    clone = document.body.cloneNode(true);
                    {exel_str}
                    return clone.textContent;
                }}"""

            if expression:
                print(f"[getters]: getting content from {page.url}")
                content += page.evaluate(f"() =>{expression}")
            add_url(page, urls, expression)

            run_scripts(page, post, urls)
    return content


def crawler(page: Page, specs: dict, urls: dict, pages: list, pre_configs: list):
    if specs:
        post = get_script(specs, "post")
        run_scripts(page, get_script(specs, "pre"), urls)

        queries = specs.get("queries") or [{"selector": "a[href]", "attribute": "href"}]
        filters = specs.get("filters") or []
        depth = specs.get("depth", 1) or 0

        if depth > 0:
            for query in queries:
                for node in page.query_selector_all(query.get("selector") or "a[href]"):
                    url = node.get_attribute(query.get("attribute") or "href")
                    c_url = get_hostname(page)

                    if url.startswith("/"):
                        url = f"{c_url}{url}"

                    if url.startswith("http") and url not in urls["crawled"]:
                        included = not bool(filters)

                        for filter in filters:
                            if search(filter, url):
                                included = True
                                break

                        if included:
                            add_crawl(
                                pages,
                                pre_configs,
                                urls,
                                url,
                                {
                                    "queries": queries,
                                    "depth": depth - 1,
                                    "filters": filters,
                                },
                            )

        run_scripts(page, post, urls)


def get_script(specs: dict, name: str):
    return specs.pop(f"{name}_scripts", []) or []


def run_scripts(page: Page, scripts: list[dict], urls: dict):
    for script in scripts:
        method = script.pop("method", "evalutate") or "evaluate"
        print(f"[script]: running method {method}\n{str(script)}")
        getattr(page, method)(**script)
        add_url(page, urls)


def add_url(page: Page, urls: dict, scraped: bool = False):
    url = page.url
    if url:
        if url not in urls["scanned"]:
            urls["scanned"].add(url)

        if scraped and url not in urls["scraped"]:
            urls["scraped"].add(url)


def add_crawl(pages: list, pre_configs: list, urls: dict, url: str, def_crawl: dict):
    urls["crawled"].add(url)
    scraper = {
        "goto": {
            "url": url,
            "wait_until": "networkidle",
            "pre_scripts": [],
            "post_scripts": [],
        },
        "getters": [{"method": "default"}],
        "crawler": def_crawl,
    }
    for pconf in pre_configs:
        if search(pconf["regex"], url):
            scraper = deepcopy(pconf["scraper"])
            (scraper.get("goto") or {})["url"] = url
            scraper["crawler"] = scraper.get("crawler") or def_crawl
            break

    pages.append(scraper)


def get_hostname(page: Page):
    url = page.url
    if url:
        splitter = url.split("//")
        protocol = splitter[0]
        hostname = splitter[1].split("/")[0]
        return f"{protocol}//{hostname}"
    return url


###########################################################################
#                               OLD SCRAPER                               #
###########################################################################


@jaseci_action(act_group=["wbs"], allow_remote=True)
def old_scrape(
    urls: set,
    scripts: dict = {},
    url_filters: list = [],
    timeout: int = 60000,
    depth: int = 1,
    detailed: bool = False,
    excluded_elem: list = ["script", "style", "link", "noscript"],
):
    all_content = ""

    scraped = set()
    with sync_playwright() as spw:
        browser = spw.chromium.launch()
        page = browser.new_page()

        while depth > 0:
            content, urls = scraping(
                page, urls, scripts, url_filters, timeout, scraped, excluded_elem
            )
            all_content += f"\n{content}"
            depth -= 1

        browser.close()

    contents = " ".join(all_content.split())

    if detailed:
        return {"contents": contents, "scraped": list(scraped)}
    return contents


def load_and_save(
    page: Page,
    target: str,
    script: Union[dict, str],
    timeout: int,
    scraped: set,
    excluded_elem: list,
):
    wait_for = script.get("wait_for")
    selector = script.get("selector")
    custom = script.get("custom")

    pre = script.get("pre") or {}
    post = script.get("post") or {}

    print("#############################")
    try:
        scraped.add(target)
        print(f"loading {target} ...")
        page.goto(target, wait_until="networkidle", timeout=timeout)

        if wait_for:
            page.wait_for_selector(**wait_for)

        run_script(page, pre, "pre")

        # print(f"capturing {target} ...")
        # page.screenshot(path="".join(x for x in target if x.isalnum()) + ".png", full_page=True)

        exclusion = ""
        for exc in excluded_elem:
            exclusion += f'clone.querySelectorAll("{exc}").forEach(d => d.remove());\n'

        query = f"""{{
            clone = document.body.cloneNode(true);
            {exclusion}
            return clone.textContent;
        }}"""
        if custom:
            query = f"{{{custom}}}"
        elif selector:
            query = f"""
                Array.prototype.map.call(
                    document.querySelectorAll("{selector}"),
                    d => {{
                        clone = d.cloneNode(true);
                        {exclusion}
                        return clone.textContent;
                    }}).join("\n");
            """

        print(f"getting relevant content using {query} ...")
        content = page.evaluate(f"() =>{query}")

        run_script(page, post, "post")

        return content
    except Exception as e:
        print(
            f"Error occurs when trying to load and save {target} ...\n{e}",
        )
        return ""


def run_script(page: Page, script: dict, title: str):
    if script:
        expr = script["expr"]
        print(f"running {title} script {expr}")
        page.evaluate(f"() =>{{{expr}}}")

        wait_for = script.get("wait_for") or {}
        if wait_for:
            page.wait_for_selector(**wait_for)

        page.wait_for_load_state("networkidle")


def crawling(page: Page):
    try:
        return page.query_selector_all("a[href]")
    except Exception as e:
        print(f"Error occurs when trying to crawl {page.url} !\n{e}")
        return []


def scraping(
    page: Page,
    urls: set,
    scripts: dict,
    url_filters: list,
    timeout: int,
    scraped: set,
    excluded_elem: list,
):
    content = ""
    next_scrape = set()

    while urls:
        url: str = urls.pop()
        if url not in scraped:
            script = {}
            for key, val in scripts.items():
                if search(key, url):
                    script = val
                    break

            content += load_and_save(page, url, script, timeout, scraped, excluded_elem)

            for ahref in crawling(page):
                href = ahref.get_attribute("href")
                if href.startswith("/"):
                    href = f"{url}{href}"

                if href.startswith("http"):
                    included = True

                    for filter in url_filters:
                        if search(filter, href):
                            included = False
                            break

                    if included:
                        next_scrape.add(href)

    return content, next_scrape
