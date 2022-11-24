---
title: Button
---

#### Summary

A `Button` will render a `jsc-button`. Under the hood, this `jsc-button` tag will render a `html` button element within it's shadow DOM.

<u>Example:</u>

```JSON
{
	"component": "Button",
	"events": {},
	"props": {
		"label": "Click me",
        "palette": "primary"
	},
	"css": {
		"background": "red"
	}
}


```

The above code will render a button with a red background and a label of "Click me".

### Props

| name            | type                                                                                                       | description |
| --------------- | ---------------------------------------------------------------------------------------------------------- | ----------- |
| label           | `string`                                                                                                   |             |
| variant         | `default` or `link`                                                                                        |             |
| size            | `sm` or `md` or `lg` or `xs`                                                                               |             |
| palette         | `primary` or `secondary` or `accent` or `info` or `warning` or `error` or `success` or `accent` or `ghost` |             |
| fullWidth       | `boolean`                                                                                                  |             |
| active          | `boolean`                                                                                                  |             |
| noRadius        | `boolean`                                                                                                  |             |
| tooltip         | `string`                                                                                                   |             |
| tooltipPosition | `bottom` or `left` or `right`                                                                              |             |
| tooltipPalette  | `primary` or `secondary` or `accent` or `info` or `warning` or `error` or `success` or `accent` or `ghost` |             |
