---
title: DatePicker
---

#### Summary

Displays a rendered list of a specified markup (template) for lists of data returned from a jaseci endpoint.

<u>Example:</u>

```JSON
{
  "name": "date",
  "component": "DatePicker",
  "props": {
    "label": "Date",
    "fullwidth": "true",
    "type": "datetime"
  }
}
```

### Props

| name      | type                 | description                                                                  |
| --------- | -------------------- | ---------------------------------------------------------------------------- |
| label     | `string`             |                                                                              |
| fullwidth | `true` or `false`    | Determines if the datepicker filed with take up the full width of its parent |
| type      | `datetime` or `date` | Date field will also collect time input if type is set to `datetime`         |
