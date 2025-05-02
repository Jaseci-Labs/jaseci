node GraphNode {
  has node_name: str;
  has visited: bool = False;
}

walker bfs {
  can run_bfs with GraphNode entry {
    print(here.node_name);
    visit [-->];
  }
}

with entry {
  r = GraphNode(node_name = "r");
  n1 = GraphNode(node_name = "n1");
  n2 = GraphNode(node_name = "n2");
  n3 = GraphNode(node_name = "n3");
  n4 = GraphNode(node_name = "n4");
  r++>n1;
  r++>n2;
  n1++>n3;
  n2++>n4;
  wlk = r spawn bfs();
}
