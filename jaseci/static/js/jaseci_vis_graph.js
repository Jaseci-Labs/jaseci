var nodeIds, shadowState, nodesArray, nodes, edgesArray, edges, network;

function startNetwork() {

    nodes = new vis.DataSet([]);
    edges = new vis.DataSet([]);

    // create a network
    var container = document.getElementById('mynetwork');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = { nodes: { shadow: true }, edges: { shadow: true } };
    network = new vis.Network(container, data, options);
}

function addNode(nid, name) {
    nodes.add({ id: nid, label: name });
}

function addEdge(bid, tid) {
    edges.add({ from: bid, to: tid });
}

function removeNode(nid) {
    nodes.remove({ id: nid });
}

function removeEdge(bid, tid) {
    edges.remove({ from: bid, to: tid });
}

function clearAll() {
    nodes.clear();
    edges.clear();
}

