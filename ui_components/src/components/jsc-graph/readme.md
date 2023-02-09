# my-component



<!-- Auto Generated Below -->


## Events

| Event                   | Description | Type                                                                         |
| ----------------------- | ----------- | ---------------------------------------------------------------------------- |
| `disableZoom`           |             | `CustomEvent<any>`                                                           |
| `enableZoom`            |             | `CustomEvent<any>`                                                           |
| `expandNode`            |             | `CustomEvent<Node & { context: {}; info: {}; details: {}; group: string; }>` |
| `expandNodeRecursively` |             | `CustomEvent<Node & { context: {}; info: {}; details: {}; group: string; }>` |
| `hideEdgeGroup`         |             | `CustomEvent<Edge & { context: {}; info: {}; details: {}; group: string; }>` |
| `hideNodeGroup`         |             | `CustomEvent<Node & { context: {}; info: {}; details: {}; group: string; }>` |


## Methods

### `hide() => Promise<void>`



#### Returns

Type: `Promise<void>`



### `setClickedItem({ clickedNode, clickedEdge }: { clickedNode?: GraphNode; clickedEdge?: GraphEdge; }) => Promise<void>`



#### Returns

Type: `Promise<void>`



### `setPos(x: number, y: number) => Promise<void>`



#### Returns

Type: `Promise<void>`



### `show() => Promise<void>`



#### Returns

Type: `Promise<void>`




## Dependencies

### Used by

 - [jsc-graph](.)

### Depends on

- [jsc-divider](../jsc-divider)
- [jsc-button](../jsc-button)

### Graph
```mermaid
graph TD;
  jsc-graph-context-menu --> jsc-divider
  jsc-graph-context-menu --> jsc-button
  jsc-graph --> jsc-graph-context-menu
  style jsc-graph-context-menu fill:#f9f,stroke:#333,stroke-width:4px
```

----------------------------------------------

*Built with [StencilJS](https://stenciljs.com/)*
