---
title: Datalist
---

#### Summary

Displays a rendered list of a specified markup (template) for lists of data returned from a jaseci endpoint.

<u>Example:</u>

```JSON
{
    "name": "datalist",
    "component": "Datalist",
    "props": {
      "server": "http://localhost:8000",
      "walker": "list_tag",
      "token": "198ab01ffecda8b09c98e2e679257d25644c430690ae0cacd54529bcd83b0b9a",
      "snt": "urn:uuid:ae422d32-27eb-4ee8-9d91-b1a6b4189caf",
      "getters": [{"name": "label", "accessor": "label" }],
      "template": [
        {
          "component": "Chip",
          "props": {
            "label": "{{label}}"
          }
        }
      ]
    }
}
```

### Props

| name     | type                                                                                        | description                                                                                                                      |
| -------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| getters  | `Array<{label: string, accessor: string, formatter?: "date" or "native", format?: string}>` | Creates placeholders for the template of the data list content where the placeholder content is replaced with the accessor value |
| server   | `string`                                                                                    | Running jac server url                                                                                                           |
| walker   | `string`                                                                                    | This walker that will be called to retrieve the data                                                                             |
| token    | `string`                                                                                    | A valid authentication token that will be used to call the endpoint                                                              |
| snt      | `string`                                                                                    |                                                                                                                                  |
| template | `Array<Component>`                                                                          | The template is rendered for each item in the list of data returned from the endpoint.                                           |
