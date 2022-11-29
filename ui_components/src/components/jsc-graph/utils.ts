import * as vis from 'vis-network';

export function formatNodes(data: [][] = []): vis.Node[] {
  return data
    ?.filter((item: any) => item.j_type === 'node')
    .map((node: any) => ({
      id: node.jid,
      label: node.name,
      group: node.name,
      context: { ...node.context, jid: node.jid },
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
      context: { ...edge.context, jid: edge.jid },
      group: edge.name,
      length: 150,
    }));

  return newEdges;
}
