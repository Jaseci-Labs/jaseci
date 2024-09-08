# my-component



<!-- Auto Generated Below -->


## Properties

| Property    | Attribute   | Description | Type       | Default     |
| ----------- | ----------- | ----------- | ---------- | ----------- |
| `nodeId`    | `nodeid`    |             | `string`   | `undefined` |
| `sentinel`  | `sentinel`  |             | `string`   | `undefined` |
| `serverUrl` | `serverurl` |             | `string`   | `undefined` |
| `walkers`   | --          |             | `Walker[]` | `undefined` |


## Events

| Event             | Description | Type                  |
| ----------------- | ----------- | --------------------- |
| `walkerCompleted` |             | `CustomEvent<string>` |


## Dependencies

### Used by

 - [jsc-graph](../jsc-graph)

### Depends on

- [jsc-inputbox](../jsc-input)
- [jsc-select](../jsc-select)

### Graph
```mermaid
graph TD;
  graph-walker-runner --> jsc-inputbox
  graph-walker-runner --> jsc-select
  jsc-graph --> graph-walker-runner
  style graph-walker-runner fill:#f9f,stroke:#333,stroke-width:4px
```

----------------------------------------------

*Built with [StencilJS](https://stenciljs.com/)*
