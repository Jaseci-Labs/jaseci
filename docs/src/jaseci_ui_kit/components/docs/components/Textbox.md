#### Summary

A `Textbox` component will render a container, `jsc-textbox`, that will a render an `textarea` element within it's DOM.

<u>Example:</u>

```JSON
{
	"component": "Textbox",
	"events": {},
	"props": {
		"placeholder": "Biography",
		"fullwidth": "true",
		"value": "Jaseci AI"
	},
	"css": {
		"padding": "0 10px"
	}
}
```

The code above will render an input with a placeholder of "Biography", it will span the full width of its parent and have its value set to 'Jaseci AI'.

#### Props

| name        | type      | description                                                    |
| ----------- | --------- | -------------------------------------------------------------- |
| placeholder | `string`  | sets the input placeholder                                     |
| value       | `string`  | will make the text input take up 100% of its parent container  |
| fullWidth   | `boolean` | will make the text input take up 100% of its parent container. |
