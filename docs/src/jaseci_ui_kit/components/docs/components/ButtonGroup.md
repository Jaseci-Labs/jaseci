---
title: ButtonGroup
---

#### Summary

Renders a group of buttons

<u>Example:</u>

```JSON
{
                  "component": "ButtonGroup",
                  "props": {
                    "buttons": [
                      {
                        "label": "Page 1",
                        "href": "http://google.com"
                      },
                      {
                        "label": "Page 2",
                        "href": "http://google.com",
                        "active": "true"
                      },
                      {
                        "label": "Page 3",
                        "href": "http://google.com"
                      }
                    ]
                  }
                }
```

### Props

| name    | type                                                     | description |
| ------- | -------------------------------------------------------- | ----------- |
| buttons | `Array<{label: string, href: string, active?: boolean}>` |             |
