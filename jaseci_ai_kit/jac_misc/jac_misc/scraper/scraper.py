from jaseci.jsorc.live_actions import jaseci_action
from playwright.sync_api import sync_playwright, Page


@jaseci_action(act_group=["ws"], allow_remote=True)
def scrape(urls: str, depth: int = 1):
    all_content = ""

    scraped = set()
    with sync_playwright() as spw:
        browser = spw.chromium.launch()
        page = browser.new_page()

        while depth > 0:
            content, urls = scraping(page, urls, scraped)
            all_content += f"\n{content}"
            depth -= 1

        browser.close()

    return " ".join(all_content.split())


def load_and_save(page: Page, target: str, scraped: set):
    print("#############################")
    try:
        scraped.add(target)
        print(f"loading {target} ...")
        page.goto(target, wait_until="networkidle")

        # print(f"capturing {target} ...")
        # page.screenshot(path="".join(x for x in target if x.isalnum()) + ".png", full_page=True)

        print(f"getting relevant content {target} ...")
        return page.evaluate(
            """() =>
            document.body.textContent;
        """
        )
    except Exception as e:
        print(
            f"Error occurs when trying to load and save {target} ...\n{e}",
        )
        return ""


def crawling(page: Page):
    try:
        return page.query_selector_all("a[href]")
    except Exception as e:
        print(f"Error occurs when trying to crawl {page.url} !\n{e}")
        return []


def scraping(page: Page, urls: set, scraped: set):
    content = ""
    next_scrape = set()

    while urls:
        url: str = urls.pop()
        if url not in scraped:
            content += load_and_save(page, url, scraped)

            for ahref in crawling(page):
                href = ahref.get_attribute("href")
                if href.startswith("http"):
                    next_scrape.add(href)
                elif href.startswith("/"):
                    next_scrape.add(f"{url}{href}")

    return content, next_scrape
