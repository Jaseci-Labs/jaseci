import { Event, Component, EventEmitter, h, Method, State, Listen, Fragment } from '@stencil/core';
import type { Node, Edge } from 'vis-network';

export type GraphNode = Node & { context: {}; info: {}; details: {}; group: string };
export type GraphEdge = Edge & { context: {}; info: {}; details: {}; group: string };
export type NodeGroupConfig = { [groupName: string]: { color?: string; displayedVar: string } };
@Component({
  tag: 'jsc-graph-context-menu',
  styleUrl: 'jsc-graph-context-menu.css',
  shadow: true,
})
export class JscGraphContextMenu {
  contextMenuEl!: HTMLDivElement;

  @State() clickedNode: GraphNode | null;
  @State() clickedEdge: GraphEdge | null;
  @State() mode: 'default' | 'configNodeGroup' = 'default';

  @State() nodeGroupConfig: NodeGroupConfig = {};

  @Event() expandNode: EventEmitter<GraphNode>;
  @Event() expandNodeRecursively: EventEmitter<GraphNode>;
  @Event() hideNodeGroup: EventEmitter<GraphNode>;
  @Event() hideEdgeGroup: EventEmitter<GraphEdge>;
  @Event() disableZoom: EventEmitter;
  @Event() enableZoom: EventEmitter;
  @Event() nodeGroupConfigChange: EventEmitter<NodeGroupConfig>;

  @Method()
  async setClickedItem({ clickedNode, clickedEdge }: { clickedNode?: GraphNode; clickedEdge?: GraphEdge }) {
    this.clickedNode = clickedNode;
    this.clickedEdge = clickedEdge;
  }

  @Method()
  async show() {
    // disable scrolling
    document.body.style.overflow = 'hidden';
    document.body.style.userSelect = 'none';

    this.disableZoom.emit();
    this.contextMenuEl.style.display = 'block';
  }

  @Method()
  async hide() {
    // enable scrolling
    document.body.style.overflow = 'auto';
    document.body.style.userSelect = 'auto';

    this.enableZoom.emit();
    this.contextMenuEl.style.display = 'none';
  }

  @Method()
  async setPos(x: number, y: number) {
    this.contextMenuEl.style.left = `${x}px`;
    this.contextMenuEl.style.top = `${y}px`;
  }

  setNodeGroupConfig(groupName: string, key: keyof NodeGroupConfig[string], value: string) {
    if (this.nodeGroupConfig[groupName] === undefined) {
      this.nodeGroupConfig[groupName] = { displayedVar: null, color: null };
    }

    this.nodeGroupConfig[groupName][key] = value;
    this.nodeGroupConfigChange.emit(this.nodeGroupConfig);
  }

  @Listen('keydown', { target: 'window' })
  handleKeyPress(event: KeyboardEvent) {
    if (event.key === 'Escape' && this.contextMenuEl.style.display === 'block') {
      this.hide();
    }
  }

  render() {
    return (
      <Fragment>
        <div>
          <div
            id="graph-context-menu"
            style={{
              position: 'absolute',
              minHeight: '120px',
              minWidth: '240px',
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
            {this.mode === 'default' && (
              <div>
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

                {this.clickedNode && (
                  <jsc-button
                    onClick={() => {
                      this.mode = 'configNodeGroup';
                    }}
                    variant="ghost"
                    size="xs"
                    block="true"
                    fullWidth="true"
                    label={`Configure Node Group`}
                  ></jsc-button>
                )}

                {this.clickedEdge && <jsc-button onClick={() => {}} variant="ghost" size="xs" block="true" fullWidth="true" label={`Copy Edge ID`}></jsc-button>}

                {this.clickedNode && <jsc-button onClick={() => {}} variant="ghost" size="xs" block="true" fullWidth="true" label={`Copy Node ID`}></jsc-button>}
              </div>
            )}

            {this.mode === 'configNodeGroup' && (
              <div>
                <jsc-divider label={`Configure ${this.clickedNode?.group} Nodes`} orientation="horizontal"></jsc-divider>
                <div>
                  <jsc-select
                    label="Display Value"
                    placeholder="Node Type"
                    size="xs"
                    options={Object.keys(this.clickedNode?.context || {}).map(key => ({ label: key, value: key })) || []}
                    onValueChanged={e => {
                      this.setNodeGroupConfig(this.clickedNode?.group, 'displayedVar', e.detail);
                    }}
                  ></jsc-select>
                </div>

                <jsc-button size="xs" style={{ marginTop: '12px' }} label="Back" onClick={() => (this.mode = 'default')}></jsc-button>
              </div>
            )}
          </div>
        </div>
      </Fragment>
    );
  }
}
