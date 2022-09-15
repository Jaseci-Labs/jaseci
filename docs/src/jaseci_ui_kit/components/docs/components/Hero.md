#### Summary

Renders a large text an image background and primary action button(s)

<u>Example:</u>

```JSON
{
    "component": "Hero",
    "props": {
      "label": "Title Text",
      "description":
        "Provident cupiditate voluptatem et in. Quaerat fugiat ut assumenda excepturi exercitationem quasi. In deleniti eaque aut repudiandae et a id nisi.",
      "action": { "label": "Learn More", "href": "http://google.com" },
      "backgroundImage": "https://cdn.mos.cms.futurecdn.net/tXr5UjKDsDBrYBQM9znb2c-1024-80.jpg.webp",
    }
}
```

### Props

| name        | type                                   | description                                 |
| ----------- | -------------------------------------- | ------------------------------------------- |
| label       | `string`                               |                                             |
| description | `Array<{href: string, label: string}>` |                                             |
| action      | `Props<{label: string, href: string}>` | Configuration for the primary action button |
