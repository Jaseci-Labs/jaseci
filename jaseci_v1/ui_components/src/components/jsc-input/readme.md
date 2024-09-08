# my-component



<!-- Auto Generated Below -->


## Properties

| Property      | Attribute     | Description | Type                                                                                                       | Default              |
| ------------- | ------------- | ----------- | ---------------------------------------------------------------------------------------------------------- | -------------------- |
| `altLabel`    | `alt-label`   |             | `string`                                                                                                   | `undefined`          |
| `css`         | `css`         |             | `string`                                                                                                   | `JSON.stringify({})` |
| `events`      | `events`      |             | `string`                                                                                                   | `undefined`          |
| `fullwidth`   | `fullwidth`   |             | `string`                                                                                                   | `undefined`          |
| `label`       | `label`       |             | `string`                                                                                                   | `undefined`          |
| `name`        | `name`        |             | `string`                                                                                                   | `undefined`          |
| `operations`  | `operations`  |             | `string`                                                                                                   | `undefined`          |
| `palette`     | `palette`     |             | `"accent" \| "error" \| "ghost" \| "info" \| "link" \| "primary" \| "secondary" \| "success" \| "warning"` | `undefined`          |
| `placeholder` | `placeholder` |             | `string`                                                                                                   | `undefined`          |
| `size`        | `size`        |             | `"lg" \| "md" \| "sm" \| "xs"`                                                                             | `undefined`          |
| `type`        | `type`        |             | `string`                                                                                                   | `'text'`             |
| `value`       | `value`       |             | `string`                                                                                                   | `undefined`          |


## Events

| Event          | Description | Type                  |
| -------------- | ----------- | --------------------- |
| `valueChanged` |             | `CustomEvent<string>` |


## Dependencies

### Used by

 - [graph-walker-runner](../graph-walker-runner)
 - [jsc-auth-form](../jsc-auth-form)
 - [jsc-date-picker](../jsc-date-picker)

### Graph
```mermaid
graph TD;
  graph-walker-runner --> jsc-inputbox
  jsc-auth-form --> jsc-inputbox
  jsc-date-picker --> jsc-inputbox
  style jsc-inputbox fill:#f9f,stroke:#333,stroke-width:4px
```

----------------------------------------------

*Built with [StencilJS](https://stenciljs.com/)*
