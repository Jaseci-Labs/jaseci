
## Container 
A Container is a general-purpose component, analogous to a div element, that will render a div you can style and attach events to.
```json
{
	"component": "Container",
	"css": {
        "width": "200px",
        "height": "200px",
	}
}
```       
## Column
 A Column is a layout component that allows you to align children components vertically. A column is rendered as a flexbox container.    
 ```json
  {
	"component": "Column",
	"events": {},
	"sections": {
		"children": []
	},
	"props": {
		"justify": "center",
		"items": "start"
	},
}                                                                  
```

The above will align the children elements in a column that's aligned to the left of the x-axis and center-aligned on the y-axis.
### Sections
- children
### Props
- justify - positions children along the y-axis
- Acceptable values are start | end | center | around | evenly
- items - positions children along the x-axis
- Acceptable values = start | end | center

## Row 
A Row is a layout component that allows you to align children components horizontally. A row is rendered as a flexbox container.
```json
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
### Sections
- children
### Props
- justify - positions children along the x-axis
- Acceptable values are start | end | center | around | evenly
- items - positions children along the y-axis
- Acceptable values = start | end | center

## Navbar 

A Navbar component will render a horizontal navigation header component ; a jsc-navbar element.
```json
{
	"component": "Navbar",
	"props": {
		"label": "Jaseci"
	}
}
```
he above will create a Navbar component with a label of 'Jaseci'.
### Sections
- links - a list of elements to render on the right side of the navbar
- Props
- label - adds a text logo to the nav

## Navlink
A Navlink component will render an anchor element within a jsc-navlink element.
```json
{
	"component": "Navlink",
	"props": {
		"label": "Home",
		"href": "/",
	}
}
```


### Props
- label
- href
- target

### Button
A Button will render a jsc-button. Under the hood, this jsc-button tag will render a html button element within it's shadow DOM. 
```json
{
	component: "Button",
	events: {},
	props: {
		label: "Click me"
	},
	css: {
		background: "red"
	},
}
```
The above code will render a button with a red background and a label of "Click me".
### Props
- label - sets the text within the button

## Input Box
An Inputbox component will render a container, jsc-inputbox, that will a render an input element within it's DOM.
```json
{
	"component": "Inputbox",
	"events": {},
	"props": {
		"placeholder": "Enter your name..."
		"fullwidth": "true",
		"value": "Jaseci",
	},
	"css": {
		"padding": "0 2px"
	},
}
```
The code above will render an input with a placeholder of "Enter your name", it will span the full width of its parent and have its value set to 'Jaseci'.
### Props
- placeholder - sets the input placeholder
- fullwidth - will make the input take up 100% of its parent container.
- value - sets the value of the input

## Text
A Text component is a that renders elements in various typographic-styles.
```json
{
	"component": "Text",
	"props": {
		"variant": "simple",
		"value": "Hello world!"
	}
}
```
### Props

- name
- type
- variant
- simple | title
- value
- string

## Textbox

A Textbox component will render a container, jsc-textbox, that will a render an textarea element within it's DOM.
{
	"component": "Textbox",
	"events": {},
	"props": {
		"placeholder": "Biography""fullwidth": "true",
		"value": "Jaseci AI",
	},
	"css": {
		"padding": "0 10px"
	},
}
The code above will render an input with a placeholder of "Biography", it will span the full width of its parent and have its value set to 'Jaseci AI'.
### Props
- placeholder
- fullwidth
- value
- Other components to document 



##Alert
##Anchor
##Authform
##Avatar
##Badge
##Breadcrumbs
##ButtonGroup
##Card
##Carousel
##checkbox
##Collapse
##DataGrid
##DataList
##DatePicker
##Dialog
##Divider
##Drawer
##DropDown
##Hero
##Input
##popover
##progress
##Radio
##RadioGroup
##Range 
##Rating
##Select
##SpeechInput 
##Stat
##Tab
##Toogle 