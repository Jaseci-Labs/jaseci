#### Summary

Allow users to rate something and collect a discrete value

<u>Example:</u>

```JSON
{
    "name": "select1",
    "component": "Select",
    "props": {
      "label": "Pet",
      "palette": "{{config:fieldPalette}}",
      "placeholder": "Choose a pet",
      "options": [{"label": "Cat" }, {"label": "Dog" }]
    }
}
```

### Props

| name        | type                                                                                                       | description |
| ----------- | ---------------------------------------------------------------------------------------------------------- | ----------- |
| label       | `string`                                                                                                   |             |
| palette     | `primary` or `secondary` or `accent` or `info` or `warning` or `error` or `success` or `accent` or `ghost` |             |
| placeholder | `string`                                                                                                   |             |
| options     | `Array<{label: string}>`                                                                                   |             |
