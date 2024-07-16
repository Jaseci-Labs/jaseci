from re import search
from uuid import uuid4, UUID
from playwright.sync_api import sync_playwright, Page

from jaseci.jsorc.jsorc import JsOrc
from jac_misc.scraper.utils import (
    Process,
    add_url,
    add_crawl,
    get_script,
    get_hostname,
)

MAX_LENGTH = 1000000  # 1,048,576 (48, 576 as buffer)


def custom_notify_client(target: str, data: dict):
    if target:
        socket = JsOrc.svc("socket")
        if socket.is_running():
            socket.notify("client", target, data)


def notify_client(
    target: str,
    trigger_id: UUID,
    pages: list,
    urls: dict,
    processing: dict,
    content=None,
):
    data = {
        "trigger_id": trigger_id,
        "processing": processing,
        "pending": [p["goto"]["url"] for p in pages],
        "scanned": urls["scanned"],
        "scraped": list(urls["scraped"]),
    }
    if content:
        data["content"] = content

    custom_notify_client(target, {"type": "scraper", "data": data})


def scrape(
    pages: list,
    pre_configs: list = [],
    detailed: bool = False,
    target: str = None,
    trigger_id: str = None,
):
    content = ""
    urls = {
        "url": pages[0]["goto"]["url"],
        "scanned": {},
        "scanned_urls": set(),
        "scraped": set(),
        "crawled": set(),
    }

    trigger_id = trigger_id or str(uuid4())

    with sync_playwright() as spw:
        browser = spw.chromium.launch()
        page = browser.new_page()

        while pages and Process.can_continue(trigger_id):
            try:
                pg: dict = pages.pop(0)

                pg_goto = pg.get("goto") or {}
                url = pg_goto.get("url") or "N/A"
                page.source = url

                Process.has_to_stop(trigger_id)

                notify_client(
                    target, trigger_id, pages, urls, {"url": url, "status": "started"}
                )

                goto(page, pg_goto, urls)

                Process.has_to_stop(trigger_id)

                content += getters(page, pg.get("getters") or [], urls)

                Process.has_to_stop(trigger_id)

                crawler(page, pg.get("crawler") or {}, urls, pages, pre_configs)

                notify_client(
                    target, trigger_id, pages, urls, {"url": url, "status": "completed"}
                )
            except Process.Stopped as e:
                add_url(page, urls, error=str(e))

                notify_client(
                    target, trigger_id, pages, urls, {"url": url, "status": "stopped"}
                )

                break
            except Exception as e:
                add_url(page, urls, error=str(e))

                notify_client(
                    target, trigger_id, pages, urls, {"url": url, "status": "failed"}
                )

        browser.close()

    content = " ".join(content.split())

    notify_client(target, trigger_id, pages, urls, None, content)

    if detailed:
        return {
            "url": urls["url"],
            "content": content,
            "scanned": urls["scanned"],
            "scraped": urls["scraped"],
        }
    return content


def goto(page: Page, specs: dict, urls: dict):
    if specs:
        post = get_script(specs, "post")
        run_scripts(page, get_script(specs, "pre"), urls)

        print(f'[goto]: loading {specs["url"]}')

        page.goto(**specs)
        add_url(page, urls, page.title())

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
                        }}).join("\\n");
                """
            elif method == "custom":
                expression = f'{{{specs.get("expression")}}}'
            elif method == "none":
                expression = ""
            else:
                expression = f"""{{
                    clone = document.body.cloneNode(true);
                    {exel_str}
                    return clone.textContent;
                }}"""

            if expression:
                print(f"[getters]: getting content from {page.url}")
                content += page.evaluate(f"() =>{expression}")
            add_url(page, urls, page.title(), expression)

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
        add_url(page, urls, page.title())


def scrape_preview(page: dict, target: str):
    with sync_playwright() as spw:
        browser = spw.chromium.launch()
        b_page = browser.new_page()
        pg_goto = page.get("goto") or {}
        post_scripts = pg_goto.pop("post_scripts", None) or []

        custom_notify_client(
            target,
            {"type": "scraper-preview", "data": {"status": "started", "data": pg_goto}},
        )

        b_page.goto(**pg_goto)
        for script in post_scripts:
            custom_notify_client(
                target,
                {
                    "type": "scraper-preview",
                    "data": {"status": "processing", "data": script},
                },
            )

            method = script.pop("method", "evalutate") or "evaluate"
            getattr(b_page, method)(**script)

        content = b_page.evaluate(f"() => document.documentElement.outerHTML")

        size = len(content)
        seq = 0
        max_seq = size - 1
        for chunks in (
            content[0 + i : MAX_LENGTH + i] for i in range(0, size, MAX_LENGTH)
        ):
            custom_notify_client(
                target,
                {
                    "type": "scraper-preview",
                    "data": {
                        "status": "finalizing",
                        "chunk": seq,
                        "max": max_seq,
                        "data": chunks,
                    },
                },
            )
            seq += 1

        custom_notify_client(
            target,
            {"type": "scraper-preview", "data": {"status": "done"}},
        )

        return content
