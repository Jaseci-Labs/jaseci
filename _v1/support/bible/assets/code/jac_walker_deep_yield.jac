walker simple_yield {
    with entry {
        t=here;
        for i=0 to i<4 by i+=1:
            t = spawn t ++> node::generic;
    }
    if(-->.length): yield take -->;
}

walker deep_yield {
    for i=0 to i<16 by i+=1 {
        spawn here walker::simple_yield;
    }
}