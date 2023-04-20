walker get_meta_valid {
    has url = "https://pypi.org/project/metadata-parser/";
    can webtool.get_page_meta;
    report webtool.get_page_meta(url);
}

walker get_meta_need_auth {
    has url = "https://docs.google.com/presentation/d/1lIYEuzzhZZ9PJaG_u3XgrFXX5Y6xd0zHV-aB2F8bXXU/edit";
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
    report webtool.get_page_meta(url);
}