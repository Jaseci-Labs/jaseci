# jsc-app



<!-- Auto Generated Below -->


## Properties

| Property | Attribute | Description | Type                | Default     |
| -------- | --------- | ----------- | ------------------- | ----------- |
| `markup` | --        |             | `JaseciComponent[]` | `undefined` |


## Events

| Event      | Description | Type                  |
| ---------- | ----------- | --------------------- |
| `onRender` |             | `CustomEvent<string>` |


## Methods

### `setGlobalConfig(config: Record<string, any> & { css: Record<string, string>; }) => Promise<void>`



#### Returns

Type: `Promise<void>`



### `setMarkup(value: any) => Promise<void>`



#### Returns

Type: `Promise<void>`




## Dependencies

### Depends on

- [jsc-graph](../jsc-graph)
- [jsc-toast](../jsc-toast)

### Graph
```mermaid
graph TD;
  jsc-app --> jsc-graph
  jsc-app --> jsc-toast
  jsc-graph --> jsc-card
  jsc-graph --> jsc-auth-form
  jsc-graph --> jsc-checkbox
  jsc-graph --> jsc-button
  jsc-graph --> jsc-divider
  jsc-graph --> jsc-chip
  jsc-graph --> jsc-select
  jsc-auth-form --> jsc-inputbox
  jsc-auth-form --> jsc-anchor
  jsc-auth-form --> jsc-button
  style jsc-app fill:#f9f,stroke:#333,stroke-width:4px
```

----------------------------------------------

*Built with [StencilJS](https://stenciljs.com/)*
