node post {has title="hi";}
edge tag_post;

walker init {
    with entry {
        for i=0 to i<10 by i+=1 {
            spawn here <+[tag_post]+> n::post(title="hi"+i.str);
        }
    }

    my_post=-->[0];
    my_post2=-->[1];

    if (my_post in <-[tag_post]->): report true; #Valid
    if (<-[tag_post]-> n::post(title==my_post.title)): report true; #Valid

    // NEED BETTER ERRORS FOR BELOW: Not Valid
    // a=<-[tag_post]-> my_post;
    // std.log(a);
    // if (<-[tag_post]-> my_post):
    //     report my_post;
    // if (<-[tag_post]-> [my_post]): report true;
}
