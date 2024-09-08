---
title: DataGrid
---

#### Summary

Display a dynamic grid of data

<u>Example:</u>

```JSON
{
                  "name": "logsDataGrid",
                  "component": "Datagrid",
                  "props": {
                    "server": "http://localhost:8000",
                    "walker": "list_log",
                    "token": "198ab01ffecda8b09c98e2e679257d25644c430690ae0cacd54529bcd83b0b9a",
                    "snt": "urn:uuid:ae422d32-27eb-4ee8-9d91-b1a6b4189caf",
                    "variant": "striped",
                    "itemsPerPage": 3,
                    "headings": [
                      { "label": "Subject", "accessor": "subject" },
                      { "label": "Message", "accessor": "body" },
                      {
                        "label": "Date",
                        "accessor": "timestamp",
                        "formatter": "date",
                        "format": "Do MMM, YYYY h:mm a",
                        "render": [{ "component": "Text", "props": { "value": "{{value}}" }, "css": { "color": "#006ADC", "fontWeight": "bold" } }]
                      },
                      {
                        "label": "Actions",
                        "accessor": "jid",
                        "render": [
                          {
                            "component": "Button",
                            "props": { "label": "Delete" },
                            "events": {
                              "onClick": [
                                {
                                  "fn": "callEndpoint",
                                  "endpoint": "http://localhost:8000/js/walker_run",
                                  "onCompleted": { "fn": "refreshDatagrid", "args": ["logsDataGrid"] },
                                  "args": [
                                    "POST",
                                    {
                                      "name": "delete_log",
                                      "snt": "urn:uuid:ae422d32-27eb-4ee8-9d91-b1a6b4189caf",
                                      "ctx": {
                                        "id": "{{value}}"
                                      }
                                    },
                                    {
                                      "Authorization": "token 198ab01ffecda8b09c98e2e679257d25644c430690ae0cacd54529bcd83b0b9a",
                                      "Content-Type": "application/json"
                                    }
                                  ]
                                }
                              ]
                            }
                          }
                        ]
                      }
                    ]
                  }
}
```

### Props

| name     | type                                                                                        | description                                                                       |
| -------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| headings | `Array<{label: string, accessor: string, formatter?: "date" or "native", format?: string}>` | Specifies the columns for the table as well as how to get the data for the column |
| server   | `string`                                                                                    | Running jac server url                                                            |
| walker   | `string`                                                                                    | This walker that will be called to retrieve the data                              |
| token    | `string`                                                                                    | A valid authentication token that will be used to call the endpoint               |
| snt      | `string`                                                                                    |                                                                                   |
| variant  | `striped` or `default`                                                                      |                                                                                   |
