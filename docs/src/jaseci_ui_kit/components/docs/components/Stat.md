#### Summary

Card for displays statistical information

<u>Example:</u>

```JSON
{
    "component": "Stat",
    "props": {
      "stats": [
        {
          "label": "Impressions",
          "value": "90,000",
          "description": "Take a look at that!"
        },
        {
          "label": "Total API Calls",
          "value": "90,000",
          "description": "You may need to upgrade soon"
        },
        {
          "label": "Unique Visitors",
          "value": "20,000",
          "description": "Going great!"
        }
      ]
    }
}

```

### Props

| name  | type                                                         | description |
| ----- | ------------------------------------------------------------ | ----------- |
| stats | `Array<{label: string, value: string, description: string}>` |             |
