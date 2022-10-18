import { Component, Element, h, Prop, State, Watch } from '@stencil/core';
import * as vis from 'vis-network';
<<<<<<< Updated upstream
=======
import * as visData from 'vis-data';
import { JscCheckboxCustomEvent } from '../../components';
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
=======
  @Prop() onFocus: 'expand' | 'isolate' = 'expand';
  @Prop() height = "100vh";
>>>>>>> Stashed changes

  // viewed node
  @State() nd = '';
  @State() network: vis.Network;

  nodes: vis.Node[];
  edges: vis.Edge[];
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
      this.nodes = this.formatNodes(data);
      this.edges = this.formatEdges(data);

      if (!this.network) {
        this.network = new vis.Network(
          this.networkEl,
          { edges: this.edges, nodes: this.nodes },
          {
            // width: '100%',
            edges: { arrows: 'to' },
            interaction: {},
          },
        );
      } else {
        this.network.setData({ edges: this.edges, nodes: this.nodes });
      }
    });
  }

  // convert response to match required format for vis
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

    this.clickedNode = this.nodes?.find((n: any) => n.id == node) as any;
    console.log(this.clickedNode);

    this.network.focus(node, {
      scale: 1.0,
      animation: { duration: 1000, easingFunction: 'easeInOutQuad' },
    });
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
    await this.getGraphState();

    this.network.on('click', params => {
      this.handleNetworkClick(this.network, params);
    });

    this.network.on('doubleClick', async params => {
      const node = this.network.getNodeAt({
        x: params?.pointer.DOM.x,
        y: params?.pointer.DOM.y,
      });

      this.nd = node.toString();
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
      <div style={{ height: this.height, width: 'auto', position: 'relative' }} data-theme="greenheart">
        {!localStorage.getItem("token") ?
          <div class="w-1/3 mx-auto my-20">
          <jsc-card title="Graph Viewer - Login">
            <jsc-auth-form  slot="children" serverURL={this.serverUrl} mode='login' redirectURL={window.location.toString()}></jsc-auth-form>
            </jsc-card>
            </div>
           :
      <div>
      <div
          style={{
<<<<<<< Updated upstream
            height: '160px',
            width: '240px',
            borderRadius: '4px',
            padding: '20px 32px',
=======
            height: '260px',
            width: '280px',
            borderRadius: '4px',
            padding: '16px',
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
          <p style={{ fontWeight: '500' }}>Context</p>
          <jsc-collapse name="Hello World!">
            <p>Hello</p>
          </jsc-collapse>
          {this.renderContext()}
=======
          <div tabindex="0" class="collapse collapse-plus border border-base-300 bg-base-100 rounded-box">
            <input type="checkbox" defaultChecked={true} />
            <div class="collapse-title text-md font-medium">Context</div>
            <div class="collapse-content">{this.renderContext()}</div>
              </div>
              
              <div tabindex="0" class="collapse collapse-plus border border-base-300 bg-base-100 rounded-box mt-2">
            <input type="checkbox" defaultChecked={true} />
            <div class="collapse-title text-md font-medium">Behaviour</div>
                <div class="collapse-content">
                  <jsc-checkbox label="Expand nodes on click" size="sm" value={String(this.onFocus === "expand")} onValueChanged={(event: JscCheckboxCustomEvent<string>) => {
                    event.detail == "true" ? this.onFocus = "expand" : this.onFocus = "isolate"
                  }}></jsc-checkbox>
            </div>
          </div>
>>>>>>> Stashed changes
        </div>
        <div style={{ position: 'absolute', top: '20px', left: '20px', zIndex: '9999' }}>
          {this.nd && <jsc-button label={'View Root'} onClick={() => (this.nd = '')}></jsc-button>}
        </div>
        <div ref={el => (this.networkEl = el)} id={'network'} style={{ height: this.height }}></div>
      </div>      
        }
      </div>
    );
  }
}
