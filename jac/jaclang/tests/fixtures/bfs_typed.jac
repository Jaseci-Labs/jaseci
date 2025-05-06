node graphnode {
  has node_name: str;
  has visited: bool = False;
}

edge SampleEdge {}

walker bfs {
  can run_bfs with graphnode entry {
    print(here.node_name);
    visit [-:SampleEdge:->];
  }
}

with entry {
  r = graphnode(node_name = "r");
  n1 = graphnode(node_name = "n1");
  n2 = graphnode(node_name = "n2");
  n3 = graphnode(node_name = "n3");
  n4 = graphnode(node_name = "n4");
  r+:SampleEdge:+>n1;
  r+:SampleEdge:+>n2;
  n1+:SampleEdge:+>n3;
  n2+:SampleEdge:+>n4;
  wlk = r spawn bfs();
}
