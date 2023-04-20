"""Built in actions for Jaseci"""
import requests
from jaseci.jsorc.live_actions import jaseci_action
from bs4 import BeautifulSoup


@jaseci_action()
def get_page_meta(url: str):
    """
    Util to parse metadata out of urls and html documents
    """
    try:
        webpage = requests.get(url)
        soup = BeautifulSoup(webpage.content, features="lxml")
        meta = soup.find_all("meta")
        meta_list = []
        for tag in meta:
            meta_list.append(dict(tag.attrs))
        return meta_list
    except Exception as e:
        print("Failed")
        return f"Failed at getting metadata for {url}: {str(e)}"
