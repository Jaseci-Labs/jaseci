import { Network } from 'vis-network';
import { JscGraph } from './jsc-graph';
import { mockFetch } from '@stencil/core/testing';
import graph_active_get from './mockData/graph_active_get.json';
import graph_node_view from './mockData/initial_graph_node_view.json';
import graph_list from './mockData/graph_list.json';

describe('jsc-graph', () => {
  afterEach(() => {
    mockFetch.reset();
  });

  test('component setup works', async () => {
    mockFetch.json(graph_active_get, 'https://api.backend.dev/js/graph_active_get');
    mockFetch.json(graph_node_view, 'https://api.backend.dev/js/graph_node_view');
    mockFetch.json(graph_list, 'https://api.backend.dev/js/graph_list');

    const graph = new JscGraph();
    const networkContainer = document.createElement('div');
    graph.serverUrl = 'https://api.backend.dev';
    graph.network = new Network(networkContainer, { edges: [], nodes: [] });
    graph.token = 'faketoken';

    // load component
    await graph.componentDidLoad();

    expect(graph.graphId).toBe('urn:uuid:b35f3240-7768-4d2f-a795-3701f78ed549');
    expect(graph.graphs.length).toBe(2);
    expect(graph.nodes.length).toBe(2);

    graph.network.destroy();
  });
});
