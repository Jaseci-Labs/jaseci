---
title: Dialog
---

#### Summary

Display a fixed container at the center of the screen. In the example below, the dialog component custom listeners (openDialog and closeDialog) which modify the `open` prop when they are triggered.

<u>Example:</u>

```JSON
{
  "components": [
        {
            "name": "myDialog",
            "component": "Dialog",
            "props": {
              "title": "This is a dialog",
              "open": "false"
            },
            "listeners": {
              "openDialog": {
                "open": "true"
              },
              "closeDialog": {
                "$call": [{ "method": "closeDialog" }]
              }
            },
            "sections": {
              "contents": [
                {
                  "component": "Text",
                  "props": {
                    "value": "Hello"
                  }
                },
                {
                  "component": "Button",
                  "props": {
                    "label": "Close this dialog"
                  },
                  "events": {
                    "onClick": [{"fn": "emit", "args": ["myDialog.closeDialog"] }]
                  }
                }
              ]
            }
          },
        {
            "name": "openDialogBtn",
            "component": "Button",
            "props": {
              "label": "Open Dialog",
              "size": "sm"
            },
            "events": {
              "onClick": [
                {
                  "fn": "emit",
                  "args": ["myDialog.openDialog"]
                }
              ]
            }
        }
    ]
}
```

### Props

| name  | type                                   | description |
| ----- | -------------------------------------- | ----------- |
| title | `string`                               |             |
| open  | `Array<{name: string, label: string}>` |             |
