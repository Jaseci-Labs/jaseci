import * as vis from 'vis-network';
import { NodeGroupConfig } from './graph-context-menu';

export function formatNodes(data: any[] = []): vis.Node[] {
  let nodeGroupConfig: NodeGroupConfig = JSON.parse(localStorage.getItem('nodeGroupConfig') || '{}');

  return data
    ?.filter((item: any) => item.j_type === 'node' || item.j_type === 'graph')
    .map((node: any) => ({
      id: node.jid,
      label: node.context[nodeGroupConfig[node.name]?.displayedVar] || node.name,
      group: node.name,
      context: { ...node.context },
      details: { j_parent: node.j_parent, j_master: node.j_master, j_access: node.j_access, dimension: node.dimension },
      info: { name: node.name, kind: node.kind, jid: node.jid, j_timestamp: node.j_timestamp, j_type: node.j_type },
      shape: 'dot',
    }));
}

// convert response to match required format for vis
export function formatEdges(data: {}[]): vis.Edge[] {
  const newEdges = data
    ?.filter((item: any) => item.j_type === 'edge' && !!item.from_node_id && !!item.to_node_id)
    .map((edge: any) => ({
      id: edge.jid,
      from: edge.from_node_id,
      to: edge.to_node_id,
      label: edge.name,
      context: { ...edge.context },
      info: { name: edge.name, kind: edge.kind, jid: edge.jid, j_timestamp: edge.j_timestamp, j_type: edge.j_type },
      details: { j_parent: edge.j_parent, j_master: edge.j_master, j_access: edge.j_access, bidirected: edge.bidirected },
      group: edge.name,
      length: 150,
    }));

  return newEdges;
}
