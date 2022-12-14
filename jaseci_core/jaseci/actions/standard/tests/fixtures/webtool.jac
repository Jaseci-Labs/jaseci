walker get_meta_valid {
    has url = "https://pypi.org/project/metadata-parser/";
    can webtool.get_page_meta;

    root {
        try {
            report webtool.get_page_meta(url);
        } else with error {
            report error;
            report:error = error;
        }
    }
}


walker get_meta_invalid {
    has url = "";
    can webtool.get_page_meta;

    root {
        try {
            report webtool.get_page_meta(url);
        } else with error {
            report error;
            report:error = error;
        }
    }
}
