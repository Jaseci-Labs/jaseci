from re import search
from copy import deepcopy


def add_url(page, urls: dict, scraped: bool = False, error: str = None):
    url = page.url
    if url:
        if url not in urls["scanned_urls"]:
            urls["scanned_urls"].add(url)

            scan = {"url": url}
            if error:
                scan["error"] = error
            urls["scanned"].append(scan)

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
