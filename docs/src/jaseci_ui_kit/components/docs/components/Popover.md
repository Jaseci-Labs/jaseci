#### Summary

Popover component

<u>Example:</u>

```JSON
{
    "name": "myPopover",
    "component": "Popover",
    "props": {
      "open": "false",
      "target": "popoverTrigger",
      "title": "A simple popover"
    },
    "sections": {
      "contents": [
        {"component": "Text", "props": { "value": "Hello!" } },
        {"component": "Text", "props": { "value": "World!" } }
      ]
    },
    "listeners": {
      "open": {
        "$call": [{"method": "openPopover" }]
      },
      "toggle": {
        "$call": [{"method": "togglePopover" }]
      }
    }
}
```

### Props

| name   | type      | description                                                     |
| ------ | --------- | --------------------------------------------------------------- |
| open   | `boolean` |                                                                 |
| target | `string`  | `name` of the component where the popover will be shown next to |
| title  | `string`  | Title of the popover container                                  |
