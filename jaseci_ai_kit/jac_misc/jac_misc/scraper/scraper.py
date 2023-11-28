from jaseci.jsorc.live_actions import jaseci_action
from playwright.sync_api import sync_playwright, Page
from typing import Union
from re import search


@jaseci_action(act_group=["wbs"], allow_remote=True)
def url_to_filename(url: str):
    return "".join(c for c in url if c.isalnum())


@jaseci_action(act_group=["wbs"], allow_remote=True)
def scrape(
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
