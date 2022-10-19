import { Component, Element, h, Prop, State, Watch } from '@stencil/core';
import * as vis from 'vis-network';
import * as visData from 'vis-data';

type EndpointBody = {
  gph?: string | null;
  nd?: string | null;
  mode?: 'default';
  detailed?: boolean;
  show_edges?: boolean;
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
  @Prop() token: string = '5eed3f010f323cd8bb6d58c14bacec2274156e82ef913b4be96e2d9d0bbffa49';
  @Prop() graphId: string = 'urn:uuid:58562489-7910-4d5a-88ec-8f4d8cd7bb22';
  @Prop() serverUrl: string = 'http://localhost:8000';
  @Prop() onFocus: 'expand' | 'isolate' = 'expand';
  @Prop() height = "100vh";

  // viewed node
  @State() nd = 'urn:uuid:153846bc-86ec-4068-8349-ec4c500241d9';
  @State() prevNd = '';
  @State() network: vis.Network;

  nodesArray: vis.Node[] = [];
  edgesArray: vis.Edge[] = [];
  edges: visData.DataSet<any, string>;
  nodes: vis.data.DataSet<any, string>;

  @State() clickedNode: vis.Node & { context: {} };

  networkEl!: HTMLDivElement;

  @Watch('nd')
  getGraphState() {
    let body: EndpointBody = { detailed: true, gph: this.graphId, mode: 'default' };
    let endpoint = `${this.serverUrl}/js/graph_get`;

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
        'Authorization': `token ${this.token}`,
      },
    }).then(async res => {
      const data = await res.json();
      if (this.nd && this.onFocus === 'expand' && this.prevNd !== '') {
        // create datasets
        if (!this.edges && !this.nodes) {
          this.nodes = new visData.DataSet([]);
          this.edges = new visData.DataSet([]);
        }

        if (this.network) {
          this.network.stabilize();
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
          if (!this.edges.get({ filter: item => item.to === edge.to }).length) {
            this.edges.add(edge);
          }
        });
      } else {
        this.nodes = new visData.DataSet(this.formatNodes(data) as any);
        this.edges = new visData.DataSet(this.formatEdges(data) as any);

        // update view when viewing the full graph
        if (this.network) {
          this.network.setData({edges: this.edges as any, nodes: this.nodes as any})
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
              dashes: true,
              selectionWidth: 2,
              width: 0.5,
              color: {},
            },
            interaction: {},
            // layout: { improvedLayout: true },
          },
        );
      } else {
        this.network.stabilize();
        this.network.storePositions();

        // this.network.setData({ edges: this.edgesArray, nodes: this.nodesArray });
        this.network.selectNodes([this.nd], true);
        this.network.focus(this.nd, { scale: 2 });
      }
    });
  }

  // convert response to match required format for vis
  @Watch('nd')
  formatNodes(data: [][]): vis.Node[] {
    return data
      ?.filter((item: any) => item.j_type === 'node')
      .map((node: any) => ({
        id: node.jid,
        label: node.name,
        group: node.name,
        context: node.context,
        shape: 'circle',
      }));
  }

  handleNetworkClick(network: vis.Network, params?: any) {
    const node = network.getNodeAt({
      x: params?.pointer.DOM.x,
      y: params?.pointer.DOM.y,
    });

    this.clickedNode = this.nodes.get([node])[0];
    console.log(this.clickedNode);
  }

  // convert response to match required format for vis
  formatEdges(data: {}[]): vis.Edge[] {
    return data
      ?.filter((item: any) => item.j_type === 'edge')
      .map((edge: any) => ({
        from: edge.from_node_id,
        to: edge.to_node_id,
        label: edge.name,
        context: edge.context,
        group: edge.name,
      }));
  }

  renderContext() {
    const context = this.clickedNode?.context;

    return context ? (
      Object.keys(this.clickedNode?.context).map(contextKey => (
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
      <div style={{ height: '500px', width: 'auto', position: 'relative' }}>
        <div
          style={{
            height: '260px',
            width: '240px',
            borderRadius: '4px',
            padding: '16px',
            top: '20px',
            right: '20px',
            position: 'absolute',
            zIndex: '9999',
            border: '2px solid #f4f4f4',
            background: '#fff',
            boxShadow: 'rgb(0 0 0 / 15%) 0px 1px 4px 0px, rgb(0 0 0 / 2%) 0px 0px 2px 1px',
            overflowY: 'auto',
            overflowX: 'hidden',
          }}
        >
          <div tabindex="0" class="collapse collapse-plus border border-base-300 bg-base-100 rounded-box">
            <input type="checkbox" defaultChecked={true} />
            <div class="collapse-title text-md font-medium">Context</div>
            <div class="collapse-content">{this.renderContext()}</div>
          </div>
        </div>
        <div style={{ position: 'absolute', top: '20px', left: '20px', zIndex: '9999' }}>
          {this.nd && <jsc-button size="sm" label={'View Full Graph'}  onClick={() => (this.nd = '')}></jsc-button>}
        </div>
        <div ref={el => (this.networkEl = el)} id={'network'} style={{ height: '100%' }}></div>
      </div>
    );
  }
}
