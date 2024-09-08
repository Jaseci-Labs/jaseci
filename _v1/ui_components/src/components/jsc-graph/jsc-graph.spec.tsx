import * as vis from 'vis-network';
import { JscGraph } from './jsc-graph';
import { mockFetch, newSpecPage } from '@stencil/core/testing';
import graph_active_get from './mockData/graph_active_get.json';
import graph_node_view from './mockData/initial_graph_node_view.json';
import graph_list from './mockData/graph_list.json';
import graph_collapse from './mockData/graph_collapse.json';
import { formatEdges, formatNodes } from './utils';
import * as visData from 'vis-data';
import { DataSet } from 'vis-data';
import { JscGraphContextMenu } from './graph-context-menu';

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
    graph.network = new vis.Network(networkContainer, { edges: [], nodes: [] });
    graph.token = 'faketoken';

    // load component
    await graph.componentDidLoad();

    expect(graph.graphId).toBe('urn:uuid:b35f3240-7768-4d2f-a795-3701f78ed549');
    expect(graph.graphs.length).toBe(2);
    expect(graph.nodes.length).toBe(2);

    graph.network.destroy();
  });

  test('component context', async () => {
    mockFetch.json(graph_active_get, 'https://api.backend.dev/js/graph_active_get');
    mockFetch.json(graph_node_view, 'https://api.backend.dev/js/graph_node_view');
    mockFetch.json(graph_list, 'https://api.backend.dev/js/graph_list');

    const graph = new JscGraph();
    const networkContainer = document.createElement('div');
    graph.serverUrl = 'https://api.backend.dev';
    graph.network = new vis.Network(networkContainer, { edges: [], nodes: [] });
    graph.token = 'faketoken';

    // load component
    await graph.componentDidLoad();

    const rootNode = graph.nodes.get()[0];
    graph.network.destroy();

    graph.clickedNode = rootNode;
  });

  test('handle collapse nodes', async () => {
    const graph = new JscGraph();
    graph.expandedNodes = ['urn:uuid:fbdb9b55-e607-4d4c-8d3e-0e6b7a248aa1', 'urn:uuid:a13be887-df9f-49bd-a7c6-f5a93839aa3b'];
    const networkContainer = document.createElement('div');
    networkContainer.style.height = '300px';
    networkContainer.style.width = '300px';

    graph.nodes = new visData.DataSet(formatNodes(graph_collapse) as any);
    graph.edges = new visData.DataSet(formatEdges(graph_collapse) as any);

    graph.network = new vis.Network(networkContainer, { edges: [], nodes: [] });

    graph.network.setOptions({ physics: { solver: 'barnesHut' } } as any);
    graph.network.setData({ nodes: graph.nodes as any, edges: graph.edges as any });

    // graph.network.setData({ nodes, edges });
    // collapse app node
    graph.handleCollapse('urn:uuid:fbdb9b55-e607-4d4c-8d3e-0e6b7a248aa1');
    expect(graph.queuedNodes.size).toBe(5);
    expect(graph.queuedEdges.size).toBe(5);

    graph.network.destroy();
  });

  test('expand node recursively', async () => {
    mockFetch.json(graph_node_view, 'https://api.backend.dev/js/graph_node_view');
    const graph = new JscGraph();
    const networkContainer = document.createElement('div');
    graph.serverUrl = 'https://api.backend.dev';
    graph.network = new vis.Network(networkContainer, { edges: [], nodes: [] });
    graph.token = 'faketoken';
    graph.graphId = 'urn:uuid:b35f3240-7768-4d2f-a795-3701f78ed549';
    graph.nodes = new DataSet(formatNodes(graph_node_view) as any);
    graph.edges = new DataSet(formatNodes(graph_node_view) as any);

    await graph.expandNodesRecursively('urn:uuid:b35f3240-7768-4d2f-a795-3701f78ed549');

    expect(graph.nodes.length).toBe(2);
  });

  test('hide nodes', async () => {
    mockFetch.json(graph_node_view, 'https://api.backend.dev/js/graph_node_view');
    const graph = new JscGraph();
    const networkContainer = document.createElement('div');
    graph.serverUrl = 'https://api.backend.dev';
    graph.token = 'faketoken';
    graph.graphId = 'urn:uuid:b35f3240-7768-4d2f-a795-3701f78ed549';
    graph.nodes = new DataSet(formatNodes(graph_node_view) as any);
    graph.edges = new DataSet(formatNodes(graph_node_view) as any);
    graph.network = new vis.Network(networkContainer, { nodes: graph.nodes as any, edges: graph.edges as any });

    graph.clickedNode = graph.nodes.get()[0];
    graph.hideNodeGroup(graph.clickedNode.group);
    expect(graph.nodes.get()[0].hidden).toBe(true);
    expect(graph.nodes.get({ filter: node => node.hidden }).length).toBeLessThan(graph.nodes.get().length);

    graph.network.destroy();
  });

  test('hide edges', async () => {
    mockFetch.json(graph_collapse, 'https://api.backend.dev/js/graph_node_view');
    const graph = new JscGraph();
    const networkContainer = document.createElement('div');
    graph.serverUrl = 'https://api.backend.dev';
    graph.token = 'faketoken';
    graph.graphId = 'urn:uuid:b35f3240-7768-4d2f-a795-3701f78ed549';
    graph.nodes = new DataSet(formatNodes(graph_node_view) as any);
    graph.edges = new DataSet(formatNodes(graph_node_view) as any);
    graph.network = new vis.Network(networkContainer, { nodes: graph.nodes as any, edges: graph.edges as any });

    graph.clickedEdge = graph.edges.get()[0];
    graph.hideEdgeGroup(graph.clickedEdge.group);
    expect(graph.edges.get()[0].hidden).toBe(true);
    expect(graph.edges.get({ filter: edge => edge.hidden }).length).toBeLessThan(graph.edges.get().length);

    graph.network.destroy();
  });

  test('handle node display value key change', async () => {
    mockFetch.json(graph_node_view, 'https://api.backend.dev/js/graph_node_view');
    const graph = new JscGraph();
    const networkContainer = document.createElement('div');
    graph.serverUrl = 'https://api.backend.dev';
    graph.network = new vis.Network(networkContainer, { edges: [], nodes: [] });
    graph.token = 'faketoken';
    graph.graphId = 'urn:uuid:b35f3240-7768-4d2f-a795-3701f78ed549';
    graph.nodes = new DataSet(formatNodes(graph_node_view) as any);
    graph.edges = new DataSet(formatNodes(graph_node_view) as any);

    console.log(graph.nodes.get({ filter: node => node.label === 'app' }));
    expect(graph.nodes.get({ filter: node => node.label === 'app' }).length).toBe(1);

    graph.handleNodeGroupConfigChange({ app: { displayedVar: 'name' } });
    expect(graph.nodes.get({ filter: node => node.label === 'Main' }).length).toBe(1);
  });
});
