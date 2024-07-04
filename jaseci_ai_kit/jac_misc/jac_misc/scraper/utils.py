from re import search
from copy import deepcopy


class Process:
    queue = set()

    class Stopped(Exception):
        pass

    @staticmethod
    def add(trigger_id: str):
        Process.queue.add(trigger_id)

    @staticmethod
    def can_continue(trigger_id: str):
        if can := (trigger_id in Process.queue):
            Process.queue.remove(trigger_id)
        return not can

    @staticmethod
    def has_to_stop(trigger_id: str):
        if trigger_id in Process.queue:
            Process.queue.remove(trigger_id)
            raise Process.Stopped()


def add_url(
    page, urls: dict, title: str = None, scraped: bool = False, error: str = None
):
    url = page.url
    source = page.source
    if url:
        if url not in urls["scanned_urls"]:
            urls["scanned_urls"].add(url)

            scan = {"title": title}
            if error:
                scan["error"] = error
            if url != source:
                scan["source"] = source
            urls["scanned"][url] = scan

        if scraped:
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


def get_hostname(page):
    url = page.url
    if url:
        splitter = url.split("//")
        protocol = splitter[0]
        hostname = splitter[1].split("/")[0]
        return f"{protocol}//{hostname}"
    return url


def get_script(specs: dict, name: str):
    return specs.pop(f"{name}_scripts", []) or []
