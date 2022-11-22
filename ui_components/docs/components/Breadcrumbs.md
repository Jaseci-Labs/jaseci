---
title: Breadcrumbs
---

#### Summary

Renders a breadcrumbs navigation component

<u>Example:</u>

```JSON

    {
          "component": "Breadcrumbs",
          "props": {
            "links": [
              {
                "label": "Apple",
                "href": "http://google.com"
              },
              {
                "label": "Oranges",
                "href": "http://example.com"
              },
              {
                "label": "Cashews"
              }
            ]
          }
    }

```

### Props

| name  | type                                   | description |
| ----- | -------------------------------------- | ----------- |
| links | `Array<{label: string, href: string}>` |             |
