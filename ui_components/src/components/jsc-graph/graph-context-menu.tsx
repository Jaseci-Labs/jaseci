import { Event, Component, EventEmitter, h, Method, State, Listen } from '@stencil/core';
import type { Node, Edge } from 'vis-network';

type GraphNode = Node & { context: {}; info: {}; details: {}; group: string };
type GraphEdge = Edge & { context: {}; info: {}; details: {}; group: string };

@Component({
  tag: 'jsc-graph-context-menu',
  styleUrl: 'jsc-graph.css',
  shadow: true,
})
export class JscGraphContextMenu {
  contextMenuEl!: HTMLDivElement;

  @State() clickedNode: GraphNode | null;
  @State() clickedEdge: GraphEdge | null;

  @Event() expandNode: EventEmitter<GraphNode>;
  @Event() expandNodeRecursively: EventEmitter<GraphNode>;
  @Event() hideNodeGroup: EventEmitter<GraphNode>;
  @Event() hideEdgeGroup: EventEmitter<GraphEdge>;
  @Event() disableZoom: EventEmitter;
  @Event() enableZoom: EventEmitter;

  @Method()
  setClickedItem({ clickedNode, clickedEdge }: { clickedNode?: GraphNode; clickedEdge?: GraphEdge }) {
    this.clickedNode = clickedNode;
    this.clickedEdge = clickedEdge;
  }

  @Method()
  show() {
    // disable scrolling
    document.body.style.overflow = 'hidden';
    document.body.style.userSelect = 'none';

    this.disableZoom.emit();
    this.contextMenuEl.style.display = 'block';
  }

  @Method()
  hide() {
    // enable scrolling
    document.body.style.overflow = 'auto';
    document.body.style.userSelect = 'auto';

    this.enableZoom.emit();
    this.contextMenuEl.style.display = 'none';
  }

  @Method()
  setPos(x: number, y: number) {
    this.contextMenuEl.style.left = `${x}px`;
    this.contextMenuEl.style.top = `${y}px`;
  }

  @Listen('keydown', { target: 'window' })
  handleKeyPress(event: KeyboardEvent) {
    if (event.key === 'Escape' && this.contextMenuEl.style.display === 'block') {
      this.hide();
    }
  }

  render() {
    return (
      <div
        id="graph-context-menu"
        style={{
          position: 'absolute',
          minHeight: '120px',
          width: '240px',
          zIndex: '2',
          borderRadius: '4px',
          padding: '16px',
          margin: 'auto 0',
          border: '2px solid #f4f4f4',
          background: '#fff',
          boxShadow: 'rgb(0 0 0 / 10%) 0px 1px 2px 0px, rgb(0 0 0 / 1%) 0px 0px 2px 1px',
          // overflowY: 'auto',
          // overflowX: 'auto',
        }}
        ref={el => (this.contextMenuEl = el)}
      >
        <jsc-divider label="Menu" orientation="horizontal"></jsc-divider>
        {this.clickedNode && (
          <jsc-button
            onClick={() => {
              this.expandNode.emit(this.clickedNode);
            }}
            variant="ghost"
            size="xs"
            block="true"
            fullWidth="true"
            label="Expand Node"
          ></jsc-button>
        )}
        {this.clickedNode && (
          <jsc-button
            onClick={() => {
              this.expandNodeRecursively.emit(this.clickedNode);
            }}
            variant="ghost"
            size="xs"
            block="true"
            fullWidth="true"
            label="Expand Node Recursively"
          ></jsc-button>
        )}

        {this.clickedNode && (
          <jsc-button
            onClick={() => this.hideNodeGroup.emit(this.clickedNode)}
            variant="ghost"
            size="xs"
            block="true"
            fullWidth="true"
            label={`Hide '${this.clickedNode?.group}' Nodes`}
          ></jsc-button>
        )}

        {this.clickedEdge && (
          <jsc-button
            onClick={() => this.hideEdgeGroup.emit(this.clickedEdge)}
            variant="ghost"
            size="xs"
            block="true"
            fullWidth="true"
            label={`Hide '${this.clickedEdge?.group}' Edges`}
          ></jsc-button>
        )}
      </div>
    );
  }
}
