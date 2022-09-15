#### Summary

Separate content with tabs

<u>Example:</u>

```JSON
{
    "name": "myTabs",
    "component": "Tabs",
    "props": {
      "variant": "lifted",
      "tabs": [
        {
          "name": "tab1",
          "label": "Home",
          "render": [{"component": "Text", "props": {"value": "Tab 1 content" } }]
        },
        {
          "name": "tab2",
          "label": "Settings",
          "render": [
            {"component": "Text", "props": { "value": "Tab 2 content" } }
          ]
        },
        {
          "name": "tab3",
          "label": "Messages",
          "render": [
            {
              "component": "Text",
              "props": { "value": "Tab 3 content" }
            }
          ]
        }
      ]
    }
  }

```

### Props

| name    | type                                                             | description             |
| ------- | ---------------------------------------------------------------- | ----------------------- |
| variant | `box` or `lifted` or `bordered` or `basic`                       |                         |
| tabs    | `Array<{name: string, label: string, render: Array<Component>}>` | List of tabs to display |
