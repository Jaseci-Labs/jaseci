---
title: DropDown
---

#### Summary

Renders a list of actions as a single component

<u>Example:</u>

```JSON
{
    "component": "Dropdown",
    "props": {
        "label": "My Dropdown",
        "items": [
            { "href": "#", "label": "Hello" },
            { "href": "#", "label": "World" }
        ],
        "buttonProps": {
            "palette": "info",
            "size": "sm"
        }
    },
    "css": {
      "marginBottom": "20px"
    }
}
```

### Props

| name        | type                                   | description                                |
| ----------- | -------------------------------------- | ------------------------------------------ |
| label       | `string`                               |                                            |
| items       | `Array<{href: string, label: string}>` |                                            |
| buttonProps | `Props<Button>`                        | Passes button props to the dropdown button |
