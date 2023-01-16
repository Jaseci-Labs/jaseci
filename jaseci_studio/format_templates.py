import argparse
import glob
import os
from bs4 import BeautifulSoup


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", type=str, required=True)
    args = parser.parse_args()
    return args


def search_and_parse(soup, tag):
    for x in soup.find_all(tag):
        if x.get("src") and x["src"].startswith("/_next/"):
            x["src"] = '{% static "' + x["src"] + '" %}'
        if x.get("href") and x["href"].startswith("/_next/"):
            x["href"] = '{% static "' + x["href"] + '" %}'
        if x.get("src") and (x["src"].endswith(".png") or x["src"].endswith(".jpg")):
            x["src"] = "/static" + x["src"]


def main():
    args = parse_args()
    for html_file in glob.glob(os.path.join(args.dir, "*html")):
        soup = BeautifulSoup(open(html_file), "html.parser")
        soup.insert(0, "{% load static %}")
        # add script to store user info into window on page load
        # is a workaround so i don't need redux
        django_script = BeautifulSoup(
            '<script>window.django = {is_authenticated: "{{ request.user.is_authenticated }}" === "True" ? true : false, user_plan: "{{user_plan}}"};</script>',
            "html.parser",
        )
        head = soup.find("head")
        head.append(django_script)
        search_and_parse(soup, "img")
        search_and_parse(soup, "link")
        search_and_parse(soup, "script")
        fout = open(html_file, "wb")
        fout.write(soup.prettify("utf-8"))
        fout.close()


main()
