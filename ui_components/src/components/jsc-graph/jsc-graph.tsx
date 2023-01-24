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

export type Walker = {
  name: string;
  kind: string;
  jid: string;
  j_timestamp: string;
  j_type: string;
  code_sig: string;
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
  @State() walkers: Walker[] = [];
  @State() serverUrl: string = localStorage.getItem('serverUrl') || 'http://localhost:8000';
  @State() hiddenNodeGroups: Set<string> = new Set();
  @State() hiddenEdgeGroups: Set<string> = new Set();
  @State() activeSentinel: string;
  @State() expandedNodes: string[] = [];

  queuedNodes: Set<string> = new Set();
  queuedEdges: Set<string> = new Set();

  nodesArray: vis.Node[] = [];
  edgesArray: vis.Edge[] = [];
  edges: visData.DataSet<any, string>;
  nodes: vis.data.DataSet<any, string>;

  @State() clickedNode: vis.Node & { context: {}; info: {}; details: {} };
  @State() clickedEdge: vis.Edge & { context: {}; info: {}; details: {}; group: string };
  @State() selectedInfoTab: 'details' | 'context' | 'info' = 'context';
  @State() selectedNodes: vis.IdType[] = [];

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
    }).then(async res => {
      return res.json();
    });
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

  async getAllWalkers(): Promise<Walker[]> {
    return await fetch(`${this.serverUrl}/js/walker_list`, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `token ${localStorage.getItem('token')}`,
      },
    }).then(res => res.json());
  }

  async getActiveSentinel(): Promise<string> {
    return await fetch(`${this.serverUrl}/js/alias_list`, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `token ${localStorage.getItem('token')}`,
      },
    })
      .then(res => res.json())
      .then(res => res['active:sentinel']);
  }

  async getGraphState() {
    let body: EndpointBody = { detailed: true, gph: this.graphId, mode: 'default', show_edges: true };
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
      const newNodes: string[] = [];
      const data = (await res.json()) || [];
      if (this.nd && this.onFocus === 'expand' && this.prevNd !== '') {
        // create datasets
        if (!this.edges && !this.nodes) {
          this.nodes = new visData.DataSet([]);
          this.edges = new visData.DataSet([]);
        }

        // expand nodes and edges sets
        this.formatNodes(data).forEach(node => {
          try {
            if (!this.nodes.get(node.id)) {
              this.nodes.add(node);
              newNodes.push(node?.id.toString());
            }
          } catch (err) {
            console.log(err);
          }
        });

        if (this.network) {
          this.network.storePositions();
        }

        this.formatEdges(data).forEach(edge => {
          const edges = this.edges.get({ filter: item => item.info.jid === (edge as any).info.jid });

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
                  max: 20,
                  drawThreshold: 5,
                  maxVisible: 25,
                },
              },
              borderWidth: 1,
            },
            interaction: {
              multiselect: true,
            },

            physics: {
              forceAtlas2Based: {
                springLength: 40,
              },
              // minVelocity: 0.2,
              solver: 'forceAtlas2Based',
            },
            // layout: { improvedLayout: true },
          },
        );
      } else {
        this.network.storePositions();
        // this.network.selectNodes([this.nd], true);
      }

      return newNodes;
    });
  }

  async expandNodesRecursively(nd: string) {
    this.nd = nd;
    this.prevNd = this.nd;
    this.expandedNodes.push(nd);

    const newNodes = await this.getGraphState();

    const newNodesPromises = newNodes.map(async node => {
      await this.expandNodesRecursively(node);
    });

    await Promise.all(newNodesPromises);
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
        filter: (node: vis.Node) => {
          return !this.queuedNodes.has(node.id.toString());
        },
      }),
    );

    // determine which nodes are to be hidden
    let hiddenNodes = this.nodes.get({
      filter: (node: vis.Node) => {
        return this.hiddenNodeGroups.has(node.group);
      },
    });

    let unhiddenNodes = this.nodes.get({
      filter: (node: vis.Node) => {
        return !this.hiddenNodeGroups.has(node.group) && node.hidden && !this.queuedNodes.has(node.id.toString());
      },
    });

    const displayedEdges = new visData.DataSet(
      this.edges.get({
        filter: (edge: vis.Edge) => {
          return !this.queuedEdges.has(edge.id.toString());
        },
      }),
    );

    this.edges = displayedEdges;
    this.nodes = displayedNodes;

    // hide nodes by setting hidden property to true
    hiddenNodes = hiddenNodes.map(node => ({ ...node, hidden: true }));
    unhiddenNodes = unhiddenNodes.map(node => ({ ...node, hidden: false }));

    console.log({ hiddenNodes });

    this.nodes.update([...hiddenNodes, ...unhiddenNodes]);

    this.network.setData({ edges: displayedEdges as any, nodes: displayedNodes as any });
  }

  refreshEdges() {
    // determine which nodes are to be hidden
    let hiddenEdges = this.edges.get({
      filter: (edge: vis.Edge & { group: string }) => {
        return this.hiddenEdgeGroups.has(edge.group);
      },
    });

    let unhiddenEdges = this.edges.get({
      filter: (edge: vis.Edge & { group: string }) => {
        return !this.hiddenNodeGroups.has(edge.group) && edge.hidden && !this.queuedNodes.has(edge.id.toString());
      },
    });

    // hide nodes by setting hidden property to true
    hiddenEdges = hiddenEdges.map(edge => ({ ...edge, hidden: true }));
    unhiddenEdges = unhiddenEdges.map(edge => ({ ...edge, hidden: false }));

    console.log({ hiddenEdges, unhiddenEdges, hiddenGroups: this.hiddenEdgeGroups });

    this.edges.update([...hiddenEdges, ...unhiddenEdges]);

    this.network.setData({ edges: this.edges as any, nodes: this.nodes as any });
  }

  hideNodeGroup() {
    if (this.clickedNode) {
      this.hiddenNodeGroups.add(this.clickedNode.group);

      // force update ui
      this.clickedNode = null;
      this.clickedNode = undefined;

      this.refreshNodes();
    }
  }

  hideEdgeGroup() {
    if (this.clickedEdge) {
      this.hiddenEdgeGroups.add(this.clickedEdge.group);

      // force update ui
      this.clickedEdge = null;
      this.clickedEdge = undefined;

      this.refreshEdges();
    }
  }

  showEdgeGroup(group: string) {
    this.hiddenEdgeGroups.delete(group);

    // force update ui
    this.clickedEdge = null;
    this.clickedEdge = undefined;

    this.refreshEdges();
  }

  showNodeGroup(group: string) {
    this.hiddenNodeGroups.delete(group);

    // force update ui
    this.clickedNode = null;
    this.clickedNode = undefined;

    this.refreshNodes();
  }

  viewRoot() {
    this.nd = '';
    this.getGraphState();
    this.expandedNodes = [this.graphId];
  }

  async collapseSelectedNodes() {
    const collapseNodesPromises = this.network.getSelectedNodes().map(async node => {
      this.prevNd = this.nd;
      this.nd = node.toString();
      this.expandedNodes = this.expandedNodes.filter(nd => nd !== this.nd).filter(nd => !this.queuedNodes.has(nd));

      this.handleCollapse(node.toString());
    });

    await Promise.all(collapseNodesPromises);

    this.refreshNodes();
    this.queuedEdges.clear();
    this.queuedNodes.clear();
  }

  async expandSelectedNodes() {
    const expandNodesPromises = this.network.getSelectedNodes().map(async node => {
      this.prevNd = this.nd;
      this.expandedNodes.push(node.toString());
      this.nd = node.toString();
      await this.getGraphState();
    });

    await Promise.all(expandNodesPromises);
  }

  handleCollapse(nodeId: string) {
    const connectedEdges = this.network.getConnectedEdges(nodeId);
    this.edges
      .get()
      .filter((edge: vis.Edge) => {
        // get the to node, so we can only collapse objects that are not hidden
        const toNode = this.nodes.get(edge.to);
        return connectedEdges.includes(edge.id) && edge.to !== nodeId && !edge.hidden && !toNode.hidden;
      })
      .forEach((edgeData: vis.Edge) => {
        // queue the nodes and edges to be removed
        this.queuedEdges.add(edgeData.id.toString());
        this.queuedNodes.add(edgeData.to.toString());

        // run the collapse on the away nodes
        this.handleCollapse(edgeData.to.toString());
      });
  }

  async componentDidLoad() {
    try {
      // set the initial graph
      let activeGraph: Graph = await this.getActiveGraph();
      this.graphId = activeGraph?.jid;

      // make root node collapsible by default
      this.expandedNodes.push(this.graphId);

      // get all graphs for the graph switcher
      this.graphs = await this.getAllGraphs();
      this.walkers = await this.getAllWalkers();
      this.activeSentinel = await this.getActiveSentinel();

      await this.getGraphState();
    } catch (err) {
      console.log(err);
    }

    this.network.on('selectNode', () => {
      this.selectedNodes = this.network.getSelectedNodes();
    });

    this.network.on('click', params => {
      // reset ui if we click on the background
      if (!params.nodes?.length && !params.edges?.length) {
        this.network.unselectAll();
        this.clickedNode = undefined;
        this.clickedEdge = undefined;
        this.selectedNodes = [];
      }

      this.handleNetworkClick(this.network, params);
    });

    this.network.on('zoom', data => {
      console.log(data);
    });

    this.network.on('doubleClick', async params => {
      this.prevNd = this.nd;

      const node = this.network.getNodeAt({
        x: params?.pointer.DOM.x,
        y: params?.pointer.DOM.y,
      });

      if (!node) return;

      this.nd = node.toString();

      console.log({ cnode: this.expandedNodes });

      if (this.expandedNodes.includes(this.nd)) {
        this.handleCollapse(node.toString());
        this.refreshNodes();
        console.log({ qnodes: this.queuedNodes });
        this.expandedNodes = this.expandedNodes.filter(nd => nd !== this.nd).filter(nd => !this.queuedNodes.has(nd));
        console.log({ cnodes: this.expandedNodes });

        // clear the queued nodes and edges to be removed
        this.queuedEdges.clear();
        this.queuedNodes.clear();
      } else {
        this.expandedNodes.push(this.nd);
        this.getGraphState();
      }
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
            <div style={{ height: this.height, maxHeight: this.height, width: 'auto', position: 'relative' }}>
              <div
                style={{
                  position: 'absolute',
                  top: '0px',
                  bottom: '0px',
                  right: '0px',
                  minWidth: '360px',
                  maxWidth: '360px',
                  height: '100%',
                  display: 'flex',
                  gap: '14px',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  paddingTop: '5px',
                  paddingBottom: '5px',
                  zIndex: '9999',
                  overflowY: 'auto',
                }}
              >
                {' '}
                <div
                  style={{
                    height: '280px',
                    width: '100%',
                    borderRadius: '4px',
                    padding: '16px',
                    border: '2px solid #f4f4f4',
                    background: '#fff',
                    boxShadow: 'rgb(0 0 0 / 10%) 0px 1px 2px 0px, rgb(0 0 0 / 1%) 0px 0px 2px 1px',
                    overflowY: 'auto',
                    overflowX: 'hidden',
                  }}
                >
                  <jsc-divider label={'Information'} orientation="horizontal"></jsc-divider>

                  {this.clickedNode || this.clickedEdge ? (
                    <graph-node-info
                      context={this.clickedNode?.context ?? this.clickedEdge?.context}
                      details={this.clickedNode?.details ?? this.clickedEdge?.details}
                      info={this.clickedNode?.info ?? this.clickedEdge?.info}
                    ></graph-node-info>
                  ) : (
                    <p>Click a node or edge to see its info</p>
                  )}
                </div>
                {this.clickedNode && (
                  <div
                    style={{
                      height: '280px',
                      width: '100%',
                      borderRadius: '4px',
                      padding: '16px',
                      margin: 'auto 0',
                      border: '2px solid #f4f4f4',
                      background: '#fff',
                      boxShadow: 'rgb(0 0 0 / 10%) 0px 1px 2px 0px, rgb(0 0 0 / 1%) 0px 0px 2px 1px',
                      overflowY: 'auto',
                      overflowX: 'auto',
                    }}
                  >
                    <jsc-divider label="Run Walker" orientation="horizontal"></jsc-divider>
                    <graph-walker-runner
                      onWalkerCompleted={async () => {
                        await this.getGraphState();
                      }}
                      walkers={this.walkers}
                      serverUrl={this.serverUrl}
                      sentinel={this.activeSentinel}
                      nodeId={this.clickedNode.id as string}
                    ></graph-walker-runner>
                  </div>
                )}
                <div
                  style={{
                    minHeight: '100px',
                    maxHeight: '200px',
                    width: '100%',
                    borderRadius: '4px',
                    padding: '16px',
                    border: '2px solid #f4f4f4',
                    background: '#fff',
                    boxShadow: 'rgb(0 0 0 / 10%) 0px 1px 2px 0px, rgb(0 0 0 / 1%) 0px 0px 2px 1px',
                    overflowY: 'auto',
                    overflowX: 'hidden',
                  }}
                >
                  <div style={{ display: 'flex', gap: '4px' }}>
                    <div>{this.clickedNode && <jsc-button size="xs" label={`Hide '${this.clickedNode.group}' Nodes`} onClick={() => this.hideNodeGroup()}></jsc-button>}</div>
                    <div>
                      {this.clickedEdge && <jsc-button size="xs" palette="info" label={`Hide '${this.clickedEdge.group}' Edges`} onClick={() => this.hideEdgeGroup()}></jsc-button>}
                    </div>
                  </div>

                  <jsc-divider label="Hidden Nodes" orientation="horizontal"></jsc-divider>
                  {!this.hiddenNodeGroups?.size && <div>No hidden nodes</div>}

                  {Array.from(this.hiddenNodeGroups).map(group => (
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

                  <jsc-divider label="Hidden Edges" orientation="horizontal"></jsc-divider>
                  {!this.hiddenEdgeGroups?.size && <div>No hidden edges</div>}
                  {Array.from(this.hiddenEdgeGroups).map(group => (
                    <div style={{ marginRight: '4px', marginBottom: '4px', display: 'inline-flex' }}>
                      <jsc-chip label={group}>
                        <svg
                          slot="right"
                          onClick={() => this.showEdgeGroup(group)}
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

              <div style={{ position: 'absolute', display: 'flex', top: '20px', left: '20px', gap: '20px', zIndex: '9999' }}>
                {this.nd && <jsc-button size="sm" label={'View Root'} onClick={() => this.viewRoot()}></jsc-button>}
                {this.selectedNodes?.length > 1 && <jsc-button size="sm" label={'Expand Nodes'} onClick={() => this.expandSelectedNodes()}></jsc-button>}
                {this.selectedNodes?.length > 1 && <jsc-button size="sm" label={'Collapse Nodes'} onClick={() => this.collapseSelectedNodes()}></jsc-button>}
                {this.selectedNodes?.length === 1 && (
                  <jsc-button size="sm" label={'Expand Recursively'} onClick={() => this.expandNodesRecursively(this.selectedNodes[0]?.toString())}></jsc-button>
                )}
              </div>

              {/*Graph Switcher*/}
              <div style={{ position: 'absolute', bottom: '20px', left: '20px', zIndex: '9999', display: 'flex', gap: '2px' }}>
                <jsc-select
                  size="sm"
                  placeholder={'Select Graph'}
                  onValueChanged={e => {
                    this.graphId = e.detail.split(':').slice(1).join(':');
                    localStorage.setItem('selectedGraph', this.graphId);
                  }}
                  options={this.graphs?.map(graph => ({ label: `${graph.name}:${graph.jid}` }))}
                ></jsc-select>

                <jsc-checkbox
                  label={'Expand nodes on click'}
                  size={'sm'}
                  value={String(this.onFocus === 'expand')}
                  onValueChanged={event => {
                    event.detail === 'true' ? (this.onFocus = 'expand') : (this.onFocus = 'isolate');
                  }}
                ></jsc-checkbox>
              </div>
              <div
                ref={el => (this.networkEl = el)}
                id={'network'}
                style={{ height: this.height, backgroundImage: 'radial-gradient(hsla(var(--bc)/.2) .5px,hsla(var(--b2)/1) .5px)', backgroundSize: '5px 5px' }}
              ></div>
            </div>
          )
        )}
      </div>
    );
  }
}
