from re import search
from playwright.sync_api import sync_playwright, Page

from jac_misc.scraper.utils import (
    notify_client,
    add_url,
    add_crawl,
    get_script,
    get_hostname,
)


def scrape(
    pages: list, pre_configs: list = [], detailed: bool = False, target: str = None
):
    content = ""
    urls = {"scanned": [], "scanned_urls": set(), "scraped": set(), "crawled": set()}

    with sync_playwright() as spw:
        browser = spw.chromium.launch()
        page = browser.new_page()

        while pages:
            try:
                pg: dict = pages.pop(0)

                pg_goto = pg.get("goto") or {}
                url = pg_goto.get("url") or "N/A"

                notify_client(target, pages, urls, {"url": url, "status": "started"})

                goto(page, pg_goto, urls)

                content += getters(page, pg.get("getters") or [], urls)

                crawler(page, pg.get("crawler") or {}, urls, pages, pre_configs)

                notify_client(target, pages, urls, {"url": url, "status": "completed"})
            except Exception as e:
                add_url(page, urls, error=str(e))

        browser.close()

    content = " ".join(content.split())

    if detailed:
        content = {
            "content": content,
            "scanned": urls["scanned"],
            "scraped": list(urls["scraped"]),
        }

    notify_client(target, pages, urls, None, content)

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


def run_scripts(page: Page, scripts: list[dict], urls: dict):
    for script in scripts:
        method = script.pop("method", "evalutate") or "evaluate"
        print(f"[script]: running method {method}\n{str(script)}")
        getattr(page, method)(**script)
        add_url(page, urls)
