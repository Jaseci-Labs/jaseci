---
title: RadioGroup
---

#### Summary

Displays a group of Radio buttons

<u>Example:</u>

```JSON
{
    "name": "radioGroup1",
    "component": "RadioGroup",
    "props": {
      "palette": "accent",
      "label": "Choose an option",
      "options": [
        { "name": "on", "label": "On" },
        { "name": "off", "label": "Off" }
      ],
      "value": "on"
    }
}

```

### Props

| name    | type                                                                                                       | description |
| ------- | ---------------------------------------------------------------------------------------------------------- | ----------- |
| label   | `string`                                                                                                   |             |
| options | `Array<{name: string, label: string}>`                                                                     |             |
| value?  | `string`                                                                                                   |             |
| palette | `primary` or `secondary` or `accent` or `info` or `warning` or `error` or `success` or `accent` or `ghost` |             |
