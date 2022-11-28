import { Component, Element, h, Prop, State, Watch } from '@stencil/core';
import * as vis from 'vis-network';
import * as visData from 'vis-data';
import { formatEdges, formatNodes } from './utils';

type EndpointBody = {
  gph?: string | null;
  nd?: string | null;
  mode?: 'default';
  detailed?: boolean;
  show_edges?: boolean;
};

type Graph = {
  name: string;
  kind: string;
  jid: string;
  j_timestamp: string;
  j_type: 'graph';
  context: Record<any, any>;
};

@Component({
  tag: 'jsc-graph',
  styleUrl: 'jsc-graph.css',
  shadow: true,
})
export class JscGraph {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() token: string = '';
  @Prop() graphId: string = '';
  @Prop() onFocus: 'expand' | 'isolate' = 'expand';
  @Prop() height = '100vh';

  // viewed node
  @State() nd = '';
  @State() prevNd = '';
  @State() network: vis.Network;
  @State() graphs: Graph[] = [];
  @State() serverUrl: string = localStorage.getItem('serverUrl') || 'http://localhost:8000';
  @State() hiddenGroups: Set<string> = new Set();

  nodesArray: vis.Node[] = [];
  edgesArray: vis.Edge[] = [];
  edges: visData.DataSet<any, string>;
  nodes: vis.data.DataSet<any, string>;

  @State() clickedNode: vis.Node & { context: {} };
  @State() clickedEdge: vis.Edge & { context: {} };

  // convert response to match required format for vis
  formatNodes = formatNodes;
  formatEdges = formatEdges;

  networkEl!: HTMLDivElement;

  async getActiveGraph(): Promise<Graph> {
    return await fetch(`${this.serverUrl}/js/graph_active_get`, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `token ${localStorage.getItem('token')}`,
      },
    }).then(res => res.json());
  }

  async getAllGraphs(): Promise<Graph[]> {
    return await fetch(`${this.serverUrl}/js/graph_list`, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `token ${localStorage.getItem('token')}`,
      },
    }).then(res => res.json());
  }

  @Watch('nd')
  async getGraphState() {
    let body: EndpointBody = { detailed: true, gph: this.graphId, mode: 'default' };
    let endpoint = `${this.serverUrl}/js/graph_node_view`;

    if (this.nd) {
      endpoint = `${this.serverUrl}/js/graph_node_view`;

      body = {
        nd: this.nd,
        show_edges: true,
        detailed: true,
      };
    }

    return fetch(endpoint, {
      method: 'post',
      body: JSON.stringify(body),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `token ${localStorage.getItem('token')}`,
      },
    }).then(async res => {
      const data = (await res.json()) || [];
      if (this.nd && this.onFocus === 'expand' && this.prevNd !== '') {
        // create datasets
        if (!this.edges && !this.nodes) {
          this.nodes = new visData.DataSet([]);
          this.edges = new visData.DataSet([]);
        }

        if (this.network) {
          // this.network.stabilize();
          this.network.storePositions();
        }

        // expand nodes and edges sets
        this.formatNodes(data).forEach(node => {
          try {
            if (!this.nodes.get(node.id)) {
              this.nodes.add(node);
            }
          } catch (err) {
            console.log(err);
          }
        });

        this.formatEdges(data).forEach(edge => {
          const edges = this.edges.get({ filter: item => item.context.jid === (edge as any).context.jid });

          if (!edges.length) {
            this.edges.add(edge);
            const fromNode = this.nodes.get({ filter: (item: vis.Node) => item.id === edge.from })[0];
            const toNode = this.nodes.get({ filter: (item: vis.Node) => item.id === edge.to })[0];

            const updates = [];

            if (fromNode) {
              updates.push({ id: fromNode.id, value: (fromNode.value || 0) + 1 });
            }

            if (toNode) {
              updates.push({ id: toNode.id, value: (toNode.value || 0) + 1 });
            }

            this.nodes.update(updates);
          }
        });
      } else {
        try {
          this.nodes = new visData.DataSet(this.formatNodes(data) as any);
          this.edges = new visData.DataSet(this.formatEdges(data) as any);
        } catch (err) {
          console.log(err);
        }

        // update view when viewing the full graph
        if (this.network) {
          this.network.setData({ edges: this.edges as any, nodes: this.nodes as any });
        }
      }

      if (!this.network) {
        this.network = new vis.Network(
          this.networkEl,
          { edges: this.edges as any, nodes: this.nodes as any },
          {
            // width: '100%',
            edges: {
              arrows: { to: { enabled: true, scaleFactor: 0.5 } },
              // dashes: true,
              selectionWidth: 2,
              width: 0.5,
              color: {},
              smooth: true,
            },
            nodes: {
              shape: 'dot',
              size: 10,
              scaling: {
                min: 10,
                max: 30,
                label: {
                  min: 10,
                  max: 25,
                  drawThreshold: 12,
                  maxVisible: 25,
                },
              },
              borderWidth: 1,
            },
            interaction: {},

            physics: {
              forceAtlas2Based: {
                springLength: 50,
              },
              minVelocity: 0.55,
              solver: 'forceAtlas2Based',
            },
            // layout: { improvedLayout: true },
          },
        );
      } else {
        this.network.storePositions();
        this.network.selectNodes([this.nd], true);
      }
    });
  }

  @Watch('graphId')
  async refreshGraph() {
    await this.getGraphState();
  }

  handleNetworkClick(network: vis.Network, params?: any) {
    const selection = network.getSelection();
    const node = network.getNodeAt({
      x: params?.pointer.DOM.x,
      y: params?.pointer.DOM.y,
    });

    const edge = network.getEdgeAt({
      x: params?.pointer.DOM.x,
      y: params?.pointer.DOM.y,
    });

    // we don't want to have a clicked edge if we click on a node
    if (selection.nodes.length) {
      this.clickedNode = this.nodes.get([node])[0];
      this.clickedEdge = undefined;
    } else {
      this.clickedEdge = this.edges.get([edge])[0];
    }
  }

  /** Update the network with the correct visibility of nodes */
  refreshNodes() {
    const displayedNodes = new visData.DataSet(
      this.nodes.get({
        filter: (item: vis.Node) => {
          return !this.hiddenGroups.has(item.group);
        },
      }),
    );

    this.network.setData({ edges: this.edges as any, nodes: displayedNodes as any });
  }

  hideNodeGroup() {
    if (this.clickedNode) {
      this.hiddenGroups.add(this.clickedNode.group);

      // force update ui
      this.clickedNode = null;
      this.clickedNode = undefined;

      this.refreshNodes();
    }
  }

  showNodeGroup(group: string) {
    this.hiddenGroups.delete(group);

    // force update ui
    this.clickedNode = null;
    this.clickedNode = undefined;

    this.refreshNodes();
  }

  renderContext() {
    let context: undefined | Record<any, any> = {};
    if (this.clickedEdge?.context) {
      context = this.clickedEdge.context;
    } else {
      context = this.clickedNode?.context;
    }

    return context ? (
      Object.keys(context).map(contextKey => (
        <div key={contextKey}>
          <p style={{ fontWeight: 'bold' }}>{contextKey}</p>
          <p>
            {Array.isArray(context[contextKey])
              ? context[contextKey].map(item => item.toString()).join(', ')
              : typeof context[contextKey] === 'boolean'
              ? context[contextKey]?.toString()
              : context[contextKey]}
          </p>
        </div>
      ))
    ) : (
      <p>Select a node or edge with contextual data</p>
    );
  }

  async componentDidLoad() {
    try {
      // set the initial graph
      let activeGraph: Graph = await this.getActiveGraph();
      this.graphId = activeGraph?.jid;

      // get all graphs for the graph switcher
      this.graphs = await this.getAllGraphs();

      await this.getGraphState();
    } catch (err) {
      console.log(err);
    }

    this.network.on('click', params => {
      this.handleNetworkClick(this.network, params);
    });

    this.network.on('doubleClick', async params => {
      this.prevNd = this.nd;

      const node = this.network.getNodeAt({
        x: params?.pointer.DOM.x,
        y: params?.pointer.DOM.y,
      });

      this.nd = node.toString();

      console.log({ nd: this.nd });
    });

    this.network.on('oncontext', params => {
      params.event.preventDefault();
      const node = this.network.getNodeAt({
        x: params.pointer.DOM.x,
        y: params.pointer.DOM.y,
      });

      if (node) {
        // this.nd = node.toString();
        // select and focus on node
        this.network.selectNodes([node]);
        this.network.focus(node, {
          scale: 1.0,
          animation: { duration: 1000, easingFunction: 'easeInOutQuad' },
        });
      }
    });
  }

  render() {
    return (
      <div data-theme={'greenheart'}>
        {!localStorage.getItem('token') ? (
          <div style={{ width: '520px', margin: '40px auto' }}>
            <jsc-card title={'Login'}>
              <jsc-auth-form
                onServerUrlChanged={e => {
                  localStorage.setItem('serverUrl', e.detail);
                  this.serverUrl = e.detail;
                }}
                slot={'children'}
                serverURL={this.serverUrl}
                redirectURL={window.location.toString()}
              ></jsc-auth-form>
            </jsc-card>
          </div>
        ) : (
          this.serverUrl && (
            <div style={{ height: this.height, width: 'auto', position: 'relative' }}>
              <div
                style={{
                  height: '260px',
                  width: '340px',
                  borderRadius: '4px',
                  padding: '16px',
                  top: '20px',
                  right: '20px',
                  position: 'absolute',
                  zIndex: '9999',
                  border: '2px solid #f4f4f4',
                  background: '#fff',
                  boxShadow: 'rgb(0 0 0 / 15%) 0px 1px 2px 0px, rgb(0 0 0 / 2%) 0px 0px 2px 1px',
                  overflowY: 'auto',
                  overflowX: 'hidden',
                }}
              >
                <div tabindex="0" class="collapse collapse-plus border border-base-300 bg-base-100 rounded-box">
                  <input type="checkbox" defaultChecked={true} />
                  <div class="collapse-title text-md font-medium">Context</div>
                  <div class="collapse-content">{this.renderContext()}</div>
                </div>

                <div tabindex={0} class={'collapse collapse-plus border border-base-300 bg-base-100 rounded-box mt-2'}>
                  <input type={'checkbox'} defaultChecked={true} />
                  <div class={'collapse-title text-md font-medium'}>Behaviour</div>
                  <div class="collapse-content">
                    <jsc-checkbox
                      label={'Expand nodes on click'}
                      size={'sm'}
                      value={String(this.onFocus === 'expand')}
                      onValueChanged={event => {
                        event.detail === 'true' ? (this.onFocus = 'expand') : (this.onFocus = 'isolate');
                      }}
                    ></jsc-checkbox>
                  </div>
                </div>

                <div tabindex={0} class={'collapse collapse-plus border border-base-300 bg-base-100 rounded-box mt-2'}>
                  <input type={'checkbox'} defaultChecked={true} />
                  <div class={'collapse-title text-md font-medium'}>Display</div>
                  <div class="collapse-content">
                    <div>{this.clickedNode && <jsc-button size="xs" label={`Hide '${this.clickedNode.group}' Nodes`} onClick={() => this.hideNodeGroup()}></jsc-button>}</div>
                    <jsc-divider label="Hidden Nodes" orientation="horizontal"></jsc-divider>
                    {Array.from(this.hiddenGroups).map(group => (
                      <div style={{ marginRight: '4px', marginBottom: '4px', display: 'inline-flex' }}>
                        <jsc-chip label={group}>
                          <svg
                            slot="right"
                            onClick={() => this.showNodeGroup(group)}
                            style={{ cursor: 'pointer' }}
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            class="inline-block w-4 h-4 stroke-current"
                          >
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                          </svg>
                        </jsc-chip>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              <div style={{ position: 'absolute', top: '20px', left: '20px', zIndex: '9999' }}>
                {this.nd && <jsc-button size="sm" label={'View Full Graph'} onClick={() => (this.nd = '')}></jsc-button>}
              </div>

              {/*Graph Switcher*/}
              <div style={{ position: 'absolute', bottom: '20px', left: '20px', zIndex: '9999' }}>
                <jsc-select
                  placeholder={'Select Graph'}
                  onValueChanged={e => {
                    this.graphId = e.detail.split(':').slice(1).join(':');
                    localStorage.setItem('selectedGraph', this.graphId);
                  }}
                  options={this.graphs?.map(graph => ({ label: `${graph.name}:${graph.jid}` }))}
                ></jsc-select>
              </div>
              <div ref={el => (this.networkEl = el)} id={'network'} style={{ height: this.height }}></div>
            </div>
          )
        )}
      </div>
    );
  }
}
