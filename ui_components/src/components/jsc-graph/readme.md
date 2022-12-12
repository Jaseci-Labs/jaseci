# my-component



<!-- Auto Generated Below -->


## Properties

| Property  | Attribute  | Description | Type                    | Default              |
| --------- | ---------- | ----------- | ----------------------- | -------------------- |
| `css`     | `css`      |             | `string`                | `JSON.stringify({})` |
| `events`  | `events`   |             | `string`                | `undefined`          |
| `graphId` | `graph-id` |             | `string`                | `''`                 |
| `height`  | `height`   |             | `string`                | `'100vh'`            |
| `onFocus` | `on-focus` |             | `"expand" \| "isolate"` | `'expand'`           |
| `token`   | `token`    |             | `string`                | `''`                 |


## Dependencies

### Used by

 - [jsc-app](../jsc-app)

### Depends on

- [jsc-card](../jsc-card)
- [jsc-auth-form](../jsc-auth-form)
- [jsc-checkbox](../jsc-checkbox)
- [jsc-button](../jsc-button)
- [jsc-divider](../jsc-divider)
- [jsc-chip](../jsc-chip)
- [graph-walker-runner](../graph-walker-runner)
- [jsc-select](../jsc-select)

### Graph
```mermaid
graph TD;
  jsc-graph --> jsc-card
  jsc-graph --> jsc-auth-form
  jsc-graph --> jsc-checkbox
  jsc-graph --> jsc-button
  jsc-graph --> jsc-divider
  jsc-graph --> jsc-chip
  jsc-graph --> graph-walker-runner
  jsc-graph --> jsc-select
  jsc-auth-form --> jsc-inputbox
  jsc-auth-form --> jsc-anchor
  jsc-auth-form --> jsc-button
  graph-walker-runner --> jsc-inputbox
  graph-walker-runner --> jsc-select
  jsc-app --> jsc-graph
  style jsc-graph fill:#f9f,stroke:#333,stroke-width:4px
```

----------------------------------------------

*Built with [StencilJS](https://stenciljs.com/)*
