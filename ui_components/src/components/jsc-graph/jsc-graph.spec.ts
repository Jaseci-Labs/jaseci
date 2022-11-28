import { Network } from 'vis-network';
import { server } from '../../mocks/server';
import { JscGraph } from './jsc-graph';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('jsc-graph', () => {
  it('component setup works', async () => {
    const graph = new JscGraph();
    const networkContainer = document.createElement('div');
    graph.serverUrl = 'http://localhost:7000';
    graph.network = new Network(networkContainer, { edges: [], nodes: [] });
    graph.token = 'faketoken';

    // load component
    graph.componentDidLoad();

    expect(graph.graphs.length).toBe(1);
  });
});
