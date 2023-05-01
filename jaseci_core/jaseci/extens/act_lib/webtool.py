"""Built in actions for Jaseci"""
import requests
from jaseci.jsorc.live_actions import jaseci_action
from bs4 import BeautifulSoup


@jaseci_action()
def get_page_meta(url: str, timeout: int = 3, parser: str = "lxml"):
    """
    Util to parse metadata out of urls and html documents
    Parser option: lxml (default), html5lib, html.parser
    Comparison between parsers: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
    """
    try:
        webpage = requests.get(
            url,
            timeout=timeout,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
            },
        )
        soup = BeautifulSoup(webpage.content, features=parser)
        meta = soup.find_all("meta")
        meta_list = []
        for tag in meta:
            meta_list.append(dict(tag.attrs))
        return meta_list
    except Exception as e:
        print("Failed")
        return f"Failed at getting metadata for {url}: {str(e)}"
