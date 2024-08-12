import websocket

from uuid import uuid4, UUID
from os import getenv
from re import search
from orjson import dumps
from json import loads
from logging import exception
from playwright.async_api import async_playwright, Page
from websocket import create_connection

from jac_misc.scraper.utils import (
    Process,
    add_url,
    add_crawl,
    get_script,
    get_hostname,
)

MAX_LENGTH = 1000000  # 1,048,576 (48, 576 as buffer)


class Client:
    def __init__(self) -> None:
        self.enabled = getenv("SCRAPER_SOCKET_ENABLED") == "true"
        self.url = getenv("SCRAPER_SOCKET_URL", "ws://jaseci-socket/ws")
        self.timeout = int(getenv("SCRAPER_SOCKET_TIMEOUT") or "2")
        self.header = {"auth": getenv("SCRAPER_SOCKET_AUTH", "12345678")}

        self.socket = None
        if self.enabled:
            self.create_connection()

    def create_connection(self) -> websocket:
        self.close()
        self.socket = create_connection(self.url, self.timeout, header=self.header)

    def close(self):
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass

    def notify_client(
        self,
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

        self.custom_notify_client(target, {"type": "scraper", "data": data})

    def custom_notify_client(self, target: str, data: dict, trial: int = 0):
        if self.enabled and self.socket and target and trial < 5:
            try:
                callback = uuid4()
                self.socket.send(
                    dumps(
                        {
                            "type": "notify_client",
                            "data": {
                                "target": target,
                                "callback": callback,
                                "data": data,
                            },
                        }
                    )
                )
                notif: dict = loads(self.socket.recv())
                if "callback" != notif.get("type") or str(callback) != notif.get(
                    "data"
                ):
                    raise Exception("Callback notification not valid!")
            except Exception:
                exception("Error sending notification!")
                self.create_connection()
                self.custom_notify_client(target, data, trial + 1)


async def scrape(
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

    ws = Client()
    trigger_id = trigger_id or str(uuid4())

    async with async_playwright() as aspw:
        browser = await aspw.chromium.launch()
        page = await browser.new_page(ignore_https_errors=True)

        while pages and Process.can_continue(trigger_id):
            try:
                pg: dict = pages.pop(0)

                pg_goto = pg.get("goto") or {}
                url = pg_goto.get("url") or "N/A"
                page.source = url

                Process.has_to_stop(trigger_id)

                ws.notify_client(
                    target, trigger_id, pages, urls, {"url": url, "status": "started"}
                )

                await goto(page, pg_goto, urls)

                Process.has_to_stop(trigger_id)

                content += await getters(page, pg.get("getters") or [], urls)

                Process.has_to_stop(trigger_id)

                await crawler(page, pg.get("crawler") or {}, urls, pages, pre_configs)

                ws.notify_client(
                    target, trigger_id, pages, urls, {"url": url, "status": "completed"}
                )
            except Process.Stopped as e:
                add_url(page, urls, error=str(e))

                ws.notify_client(
                    target, trigger_id, pages, urls, {"url": url, "status": "stopped"}
                )

                break
            except Exception as e:
                add_url(page, urls, error=str(e))

                ws.notify_client(
                    target, trigger_id, pages, urls, {"url": url, "status": "failed"}
                )

        await browser.close()

    content = " ".join(content.split())

    ws.notify_client(target, trigger_id, pages, urls, None, content)
    ws.close()

    if detailed:
        return {
            "url": urls["url"],
            "content": content,
            "scanned": urls["scanned"],
            "scraped": urls["scraped"],
        }

    return content


async def goto(page: Page, specs: dict, urls: dict):
    if specs:
        post = get_script(specs, "post")
        await run_scripts(page, get_script(specs, "pre"), urls)

        print(f'[goto]: loading {specs["url"]}')

        await page.goto(**specs)
        add_url(page, urls, await page.title())

        await run_scripts(page, post, urls)


async def getters(page: Page, specss: list[dict], urls: dict):
    content = ""
    for specs in specss:
        if specs:
            post = get_script(specs, "post")
            await run_scripts(page, get_script(specs, "pre"), urls)

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
                content += await page.evaluate(f"() =>{expression}")
            add_url(page, urls, await page.title(), expression)

            await run_scripts(page, post, urls)

    return content


async def crawler(page: Page, specs: dict, urls: dict, pages: list, pre_configs: list):
    if specs:
        post = get_script(specs, "post")
        await run_scripts(page, get_script(specs, "pre"), urls)

        queries = specs.get("queries") or [{"selector": "a[href]", "attribute": "href"}]
        filters = specs.get("filters") or []
        depth = specs.get("depth", 1) or 0

        if depth > 0:
            for query in queries:
                for node in await page.query_selector_all(
                    query.get("selector") or "a[href]"
                ):
                    url = await node.get_attribute(query.get("attribute") or "href")
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

        await run_scripts(page, post, urls)


async def run_scripts(page: Page, scripts: list[dict], urls: dict):
    for script in scripts:
        method = script.pop("method", "evalutate") or "evaluate"
        print(f"[script]: running method {method}\n{str(script)}")
        await getattr(page, method)(**script)
        add_url(page, urls, await page.title())


async def scrape_preview(page: dict, target: str = None):
    ws = Client()

    async with async_playwright() as aspw:
        browser = await aspw.chromium.launch()
        b_page = await browser.new_page()
        pg_goto = page.get("goto") or {}
        post_scripts = pg_goto.pop("post_scripts", None) or []

        ws.custom_notify_client(
            target,
            {"type": "scraper-preview", "data": {"status": "started", "data": pg_goto}},
        )

        await b_page.goto(**pg_goto)
        for script in post_scripts:
            ws.custom_notify_client(
                target,
                {
                    "type": "scraper-preview",
                    "data": {"status": "processing", "data": script},
                },
            )

            method = script.pop("method", "evalutate") or "evaluate"
            await getattr(b_page, method)(**script)

        content = await b_page.evaluate(f"() => document.documentElement.outerHTML")

        size = len(content)
        seq = 0
        max_seq = size - 1
        for chunks in (
            content[0 + i : MAX_LENGTH + i] for i in range(0, size, MAX_LENGTH)
        ):
            ws.custom_notify_client(
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

        ws.custom_notify_client(
            target,
            {"type": "scraper-preview", "data": {"status": "done"}},
        )

        return content
