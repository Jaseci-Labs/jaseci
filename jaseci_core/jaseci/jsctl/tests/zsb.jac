node botset;
node bot { has anchor name, description, metadata; }
node log_chunk { has history; }
node category { has name; }
node answer {
    has text, show_text, encoding;
    has qlinks, hitcount;
}

walker similar_questions {
    has text, thresh;
    can use.get_embedding, use.dist_score;
    with entry{if(not thresh): thresh=.1;}

    log_chunk {
        enc=use.get_embedding(text);
        for i in here.history:
            if(use.dist_score(enc,i[1])<thresh): report i;
    }
}

walker get_bots {
    root { take --> node::botset; }
    botset { report -->; disengage; }
}

walker add_bot {
    has name,desc;
    root { take --> node::botset; }
    botset {
        bot=spawn here --> node::bot(name=name,description=desc);
        report bot;
        disengage;
    }
}

walker delete_bot {
    bot, category, answer {
        take --> ;
        destroy here;
    }
}

walker change_bot {
    has name,desc;
    bot {
        here.name=name;
        here.description=desc;
        report here;
        disengage;
    }
}

walker get_answers {
    bot {
        report --> node::answer;
        take --> node::category;
    }
    category {
        report here;
        report --> node::answer;
        take --> node::category;
    }
}

walker create_answer {
    has text;
    can use.enc_answer;

    bot, category {
        ans = spawn here --> node::answer(text=text,show_text=text);
        ans.encoding = use.enc_answer(text);
        report ans;
        disengage;
    }
}

walker create_many_answers {
    has textlist;

    bot, category {
       for i in textlist: spawn here walker::create_answer(text=i,show_text=i);
    }
}

walker delete_answer {
    answer {
        destroy here;
    }
}


walker change_answer {
    has text,show_text;
    can use.enc_answer;

    answer {
        here.text = text;
        here.encoding =  use.enc_answer(text);
        here.show_text = show_text;
        report here;
    }
}


walker ask_question {
    has text, selected;
    has max_score, thisbot, dont_log, metadata;
    can use.enc_question, use.qa_score;

    with entry {
        enc=use.enc_question(text);
        selected = false;
        max_score=0; thisbot=here;
    }
    bot, category {

        for i in --> node::answer{
            score=use.qa_score(enc, i.encoding);
            if(score[0][0]>max_score){
                selected = i;
                max_score=score[0][0];
            }
        }
        take --> node::category;
    }

    with exit {
        if(not dont_log):
            spawn thisbot walker::log_question(text=text, selected=selected, metadata=metadata);
        if(selected.hitcount): selected.hitcount+=1;
        else: selected.hitcount=1;
        report selected;
    }
}

walker log_question {
    has text, selected, metadata;
    bot {
        take --> node::log_chunk else {
                spawn here --> node::log_chunk;
                take --> node::log_chunk;
            }
    }

    log_chunk {
        if(not here.history): here.history=[];
        here.history = [[std.time_now(), text, &selected, selected.text, metadata]] + here.history;
    }
}

walker get_log {
    bot {
        take --> node::log_chunk;
    }
    log_chunk {
        report here.history;
    }

}


walker link_question {
    has text;
    can use.enc_answer, use.dist_score;

    with entry{allow_multiple=false;}

    answer {
        if(here.qlinks){if(not text in here.qlinks): here.qlinks += [text];}
        else: here.qlinks = [text];
        pretext="";
        if(here.qlinks){for i in here.qlinks: pretext+=i;}
        old_enc = here.encoding;
        here.encoding = use.enc_answer(pretext+text);
        report use.dist_score(old_enc, here.encoding);
    }
}

walker get_question_matches {
    has text, num_matches, matches;
    can use.enc_question, use.qa_score;

    with entry {matches=[];}

    bot {
        enc=use.enc_question(text);
        for i in --> node::answer{
            score=use.qa_score(enc, i.encoding);
            matches += [[score[0][0], &i]];
        }
        take --> node::category;
    }

    with exit {
        if(num_matches>matches.length):
            num_matches=matches.length;
        matches=std.sort_by_col(matches, 0, 'reverse');
        for i=0 to i<num_matches by i+=1:
            report matches[i];
    }
}

walker init {
    root {
        take (--> node::botset) else {
            spawn here --> node::botset;
            std.log(-->);
            disengage;
        }
    }
}


node data_nugget { has anchor name, data; }
walker create_nugget { has name, data; spawn here --> node::data_nugget(name=name, data=data); }
walker get_nugget {has name; report --> node::data_nugget == name;}
walker delete_nugget {has name; destroy --> node::data_nugget == name;}
walker update_nugget {has name, data; n= --> node::data_nugget == name; if(n): n.data=data;}

graph sample {
    has anchor key_node;
    spawn {
        key_node = spawn node::bot(name="test");
        spawn key_node walker::create_answer(text="I like stuff");
        spawn key_node walker::create_answer(text="I am 10 years old");
        spawn key_node walker::create_answer(text="Jesus is old as shit");
        spawn key_node walker::create_answer(text="My dog is 4 years old");
    }
}

walker test {
    root { take -->; }
    botset { spawn here --> graph::sample; }
}