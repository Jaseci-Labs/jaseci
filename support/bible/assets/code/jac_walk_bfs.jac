node plain {
    has name;
}

graph example {
    has anchor head;
    spawn {
        n=[];
        for i=0 to i<7 by i+=1 {
            n.l::append(spawn node::plain(name=i+1));
        }
        n[0] --> n[1] --> n[2];
                 n[1] --> n[3];
        n[0] --> n[4] --> n[5];
                 n[4] --> n[6];
        head=n[0];
    }
}

walker init {
    root {
        spawn here --> graph::example;
    }

    plain: report here.name;
    take:bfs -->;
}