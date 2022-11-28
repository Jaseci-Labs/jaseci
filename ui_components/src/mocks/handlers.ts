import { DefaultRequestMultipartBody, MockedRequest, rest, RestHandler } from 'msw';
import graph_list from '../components/jsc-graph/mockData/graph_list.json';
import graph_active_get from '../components/jsc-graph/mockData/graph_list.json';
import initial_graph_node_view from '../components/jsc-graph/mockData/initial_graph_node_view.json';

export const handlers: Array<RestHandler<MockedRequest<DefaultRequestMultipartBody>>> = [
  rest.post('http://localhost:7000/js/graph_active_get', (_req, res, ctx) => {
    return res(ctx.json(graph_active_get));
  }),
  rest.post('http://localhost:7000/js/graph_list', (_req, res, ctx) => {
    return res(ctx.json(graph_list));
  }),
  rest.post('http://localhost:7000/js/graph_node_view', (_req, res, ctx) => {
    return res(ctx.json(initial_graph_node_view));
  }),
];
