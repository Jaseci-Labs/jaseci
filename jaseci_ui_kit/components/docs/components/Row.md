---
title: Row
---

#### Summary

A `Row` is a layout component that allows you to align `children` components horizontally. A row is rendered as a flexbox container.

<u>Example:</u>

```JSON
{
	"component": "Row",
	"events": {},
	"sections": {
		"children": []
	},
	"props": {
		"justify": "center",
		"items": "start"
	}
}
```

The above will align the children elements in a row that's center-aligned on the x-axis and aligned at the top of the y-axis.

#### Sections

- children

#### Props

| name    | type                                                 | description                         |
| ------- | ---------------------------------------------------- | ----------------------------------- |
| justify | `start` or `end` or `center` or `around` or `evenly` | positions children along the x-axis |
| items   | `start` or `end` or `center`                         | positions children along the y-axis |
