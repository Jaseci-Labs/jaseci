walker test_scraper {
    can wbs.scrape, file.url_to_filename;
    report file.url_to_filename("https://www.google.com/search?q=speed+test");
    report wbs.scrape(pages = [{
        "goto": {
            "url": "https://www.google.com/search?q=speed+test"
        },
        "getters": [{
            "method": "default"
        }],
        "crawler": {
            "filters": ["fiber.google\\.com"],
            "depth": 1
        }
    }], detailed = true);
}