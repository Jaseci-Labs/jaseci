walker get_meta_valid {
    has url = "https://pypi.org/project/metadata-parser/";
    can webtool.get_page_meta;
    report webtool.get_page_meta(url);
}

walker get_meta_need_auth {
    has url = "https://github.com/settings/profile";
    can webtool.get_page_meta;
    report webtool.get_page_meta(url);
}


walker get_meta_invalid {
    has url = "";
    can webtool.get_page_meta;
    report webtool.get_page_meta(url);
}

walker get_meta_timeout {
    has url = "https://httpstat.us/504?sleep=60000";
    can webtool.get_page_meta;
    report webtool.get_page_meta(url);
}

walker get_meta_need_header {
    has url = "https://www.invaluable.com/blog/what-is-a-mandala/";
    can webtool.get_page_meta;
    report webtool.get_page_meta(url, headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
    });
}