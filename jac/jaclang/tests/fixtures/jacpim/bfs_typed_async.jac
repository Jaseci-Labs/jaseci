node graphnode {
  has node_name: str;
  has visited: bool = False;
}

edge async_SampleEdge {}

walker bfs {
  can run_bfs with graphnode entry {
    print(here.node_name);
    visit [-:async_SampleEdge:->];
  }
}

with entry {
  r = graphnode(node_name = "r");
  n1 = graphnode(node_name = "n1");
  n2 = graphnode(node_name = "n2");
  n3 = graphnode(node_name = "n3");
  n4 = graphnode(node_name = "n4");
  r+:async_SampleEdge:+>n1;
  r+:async_SampleEdge:+>n2;
  n1+:async_SampleEdge:+>n3;
  n2+:async_SampleEdge:+>n4;
  wlk = r spawn bfs();
}
