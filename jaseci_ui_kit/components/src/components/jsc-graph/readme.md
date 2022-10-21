# my-component



<!-- Auto Generated Below -->


## Properties

| Property            | Attribute            | Description | Type                  | Default              |
| ------------------- | -------------------- | ----------- | --------------------- | -------------------- |
| `css`               | `css`                |             | `string`              | `JSON.stringify({})` |
| `events`            | `events`             |             | `string`              | `undefined`          |
| `hideNameField`     | `hidenamefield`      |             | `string`              | `'false'`            |
| `mode`              | `mode`               |             | `"login" \| "signup"` | `'login'`            |
| `name`              | `name`               |             | `string`              | `undefined`          |
| `operations`        | `operations`         |             | `any`                 | `undefined`          |
| `redirectURL`       | `redirect-u-r-l`     |             | `string`              | `undefined`          |
| `requireActivation` | `require-activation` |             | `"false" \| "true"`   | `'false'`            |
| `serverURL`         | `serverurl`          |             | `string`              | `undefined`          |
| `tokenKey`          | `tokenkey`           |             | `string`              | `'token'`            |


## Dependencies

### Depends on

- [jsc-inputbox](../jsc-input)
- [jsc-button](../jsc-button)

### Graph
```mermaid
graph TD;
  jsc-auth-form --> jsc-inputbox
  jsc-auth-form --> jsc-button
  style jsc-auth-form fill:#f9f,stroke:#333,stroke-width:4px
```

----------------------------------------------

*Built with [StencilJS](https://stenciljs.com/)*
