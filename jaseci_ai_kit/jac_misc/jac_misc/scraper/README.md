# **SCRAPER (`Playwright Python`)**
## **`!IMPORTANT!`**
remote action scraper needs to be run via `FastAPI` instead of `jaseci serv_action`. Remote action runs via uvicorn and this will require running playwright asynchronously and currently, remote action use non async function hence creating dedicated async scrape api. This is to allow local and remote scraper.
To run remotely:
```bash
export SCRAPER_SOCKET_ENABLED=true
export SCRAPER_SOCKET_URL=ws://your-websocket/ws # defaults to ws://jaseci-socket/ws
uvicorn jac_misc.scraper:app --host 0.0.0.0 --port 80 --reload
```

## wbs.**`scrape`**
> **`Arguments`:** \
> **pages**: list (structure below) \
> **pre_configs**: list (structure below)\
> **detailed**: bool = False\
> **target**: str = None
>
> **`Return`:** \
> str or dict
>
> **`Usage`:** \
> To scrape specified url
>
> **`Remarks`:** \
> **detailed** true will return dict with scanned/scraped urls\
> **target** optional client id for websocket progress notifications
>
##### **`STRUCTURE`**
```python
###########################################################################
#                             pages structure                             #
###########################################################################
[{
    # required
    # https://playwright.dev/python/docs/api/class-page#page-goto
    # this will load the targeted URL
    "goto": {
        #required
        "url": "",
        "wait_until": "networkidle",

        # -- these next fields will be popped before goto is called --

        # optional
        # all pre and post scripts have same structure
        "pre_scripts": [{
            # methods from playwright.sync_api.Page
            # https://playwright.dev/python/docs/api/class-page#methods
            "method": "wait_for_selector",

            # all other fields other than "method" will be used as **kwargs
            "**": "value"
        }],
        # optional
        "post_scripts": []
    },

    # optional
    # this will be used for scraping the loaded page
    "getters": [{
        # "selector" | "custom" | "none" | else default
        "method": "default",

        # optional
        # selector == css query selector to target element where to trigger textContent
        # custom == your custom js script that will return string
        # none == empty
        # anything else == whole document.body
        # only works with selector and custom
        "expression": "",

        # optional
        # defaults to ["script", "style", "link", "noscript"]
        # element to remove before textContent
        # only works with method selector and default
        "excluded_element": [],

        # optional
        "pre_scripts": [],
        # optional
        "post_scripts": []
    }],

    # optional
    # this option is for scraping clickable navigation such "a tag" with href
    # this urls will be appended to pages field with default structure unless found matched in pre_configs
    # you may use pre_configs to use different structure matched to your preferred regex
    "crawler": {
        # required
        # list of query selection with different attributes
        "queries": [{
                # css query selector
                "selector": "",
                # element attributes where we can get the url for crawling
                "attribute": ""
        }],

        # list of regex string that will be included in crawler
        # empty will allow everything
        "filters": [],

        # depth of crawl default to zero
        # zero will stop crawling
        "depth": 1,

        "pre_scripts": [],
        "post_scripts": []
    }
}]

###########################################################################
#                          pre_configs structure                          #
###########################################################################
[{
    # if crawled url matched to this regex, scraper field will be the structured used to append in pages field
    "regex": "",

    # similar to pages structure without goto.url
    "scraper": {
        "goto": {
            "wait_until": "networkidle",
            "pre_scripts": [],
            "post_scripts": []
        }
    }
}]
```

##### **`HOW TO TRIGGER`**
```python
wbs.scrape(
    pages = [{
        "goto": {
            "url": "http://google.com",
            "wait_until": "networkidle",
            "pre_scripts": [],
            "post_scripts": [{
                "method": "evaluate",
                "expression": """
                try {
                    document.querySelector("textarea[id=APjFqb]").value = "speed test";
                    document.querySelector("form[action='/search']:has(input[type=submit][value='Google Search'])").submit();
                } catch (err) { }
                """
            },{
                "method": "wait_for_selector",
                "selector": "#result-stats",
                "state": "visible"
            }]
        },
        "getters": [{
            "method": "default",
        }],
        "crawler": {
            "filters": ["^((?!google\\.com).)*$"],
            "depth": 1
        }
    }],
    pre_configs = [{
        "regex": "speedtest\\.net",
        "scraper": {
            "goto": {
                "wait_until": "load"
            },
            "getters": [{
                "method": "default",
            }],
        }
    },{
        "regex": "fast\\.com",
        "scraper": {
            "goto": {
                "wait_until": "load"
            },
            "getters": [{
                "method": "default",
            }],
        }
    },{
        "regex": "speedcheck\\.org",
        "scraper": {
            "goto": {
                "wait_until": "load"
            },
            "getters": [{
                "method": "default",
            }],
        }
    }],
    detailed = True
)
```