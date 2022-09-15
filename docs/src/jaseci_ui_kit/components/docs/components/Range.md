#### Summary

Collect input from a specified range of values

<u>Example:</u>

```JSON
{
    "name": "range1",
    "component": "Range",
    "props": {
      "label": "Change Threshold",
      "palette": "palette",
      "min": 0,
      "max": 100,
      "defaultValue": 80
    }
}
```

### Props

| name         | type                                                                                                       | description |
| ------------ | ---------------------------------------------------------------------------------------------------------- | ----------- |
| label        | `string`                                                                                                   |             |
| palette      | `primary` or `secondary` or `accent` or `info` or `warning` or `error` or `success` or `accent` or `ghost` |             |
| min          | `number`                                                                                                   |             |
| max          | `number`                                                                                                   |             |
| defaultValue | `number`                                                                                                   |             |
