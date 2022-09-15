#### Summary

Separate content into collapsable sections

<u>Example:</u>

```JSON
    {
            "component": "Collapse",
            "props": {
              "label": "How do I use Jaseci?",
              "palette": "primary",
              "defaultValue": "80"
            },
            "sections": {
              "children": [
                { "component": "Text", "props": { "value": "Visit the site to learn more: " } },
                {
                  "component": "Anchor",
                  "props": {
                    "label": "Click Here",
                    "palette": "primary",
                    "href": "https://docs.jaseci.org/"
                  }
                }
              ]
            }
      }
```

### Props

| name    | type                                 | description |
| ------- | ------------------------------------ | ----------- |
| label   | `string`                             |             |
| palette | `primary` or `secondary` or `accent` |             |
| icon    | `plus` or `arrow`                    |             |

### Sections

| name     | description                                               |
| -------- | --------------------------------------------------------- |
| children | Hidden content when the component is in a collapsed state |
