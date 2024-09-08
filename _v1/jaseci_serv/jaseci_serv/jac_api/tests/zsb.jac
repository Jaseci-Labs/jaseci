node botset {has bug_check, bug_check_deep={'a': {'b': [3]}};}

node bot { has anchor name; }
node log_chunk { has history; }

node answer {
    has text, show_text, encoding;
    has qlinks;
}

walker get_bots {

    root { take --> node::botset; }
    botset { report -->; disengage; }
}

walker add_bot {
    has name;
    root { take --> node::botset; }
    botset {
        bot=spawn here ++> node::bot(name=name);
        report bot;
    }
}

walker delete_bot {
    bot, answer {
        take --> ;
        destroy here;
    }
}


walker get_answers {
    bot {
        report -->;
        disengage;
    }
}

walker create_answer {
    has text, show_text;
    can use.enc_answer;

    bot {
        ans = spawn here ++> node::answer(text=text, show_text=show_text);
        ans.encoding = use.enc_answer(text);
        report ans;
        disengage;
    }
}

walker link_question {
    has text;
    can use.enc_answer, use.dist_score;

    answer {
        if(here.qlinks): here.qlinks += [text];
        else: here.qlinks = [text];
        pretext="";
        if(here.qlinks){for i in here.qlinks: pretext+=i;}
        old_enc = here.encoding;
        here.encoding = use.enc_answer(pretext+text);
        report use.dist_score(old_enc, here.encoding);
    }
}

walker unlink_question {
    has idx;
    can use.enc_answer, use.dist_score;

    answer {
        if(not here.qlinks or here.qlinks.length < idx):
            report "Index out of range!";
        else {
            destroy here.qlinks[idx];
            pretext="";
            for i in here.qlinks: pretext+=i;
            old_enc = here.encoding;
            here.encoding = use.enc_answer(pretext+text);
            report use.dist_score(old_enc, here.encoding);
        }
    }
}

walker delete_answer {
    answer {
        destroy here;
    }
}

walker change_answer {
    has text;
    can use.enc_answer;

    answer {
        here.text = text;
        pretext="";
        if(here.qlinks){for i in here.qlinks: pretext+=i;}
        here.encoding = use.enc_answer(pretext+text);
        report here;
        disengage;
    }
}

walker ask_question {
    has text, selected;
    can use.enc_question, use.qa_score;

    with entry {
        enc=use.enc_question(text);
        selected = false;
    }

    bot {
        max_score = 0;
        for i in --> node::answer {
            score=use.qa_score(enc, i.encoding);
            if(score[0][0]>max_score){
                selected = i;
                max_score=score[0][0];
            }
        }
        take --> node::log_chunk else {
            spawn here ++> node::log_chunk;
            take --> node::log_chunk;
        }
    }

    log_chunk {
        if(not here.history): here.history=[];
        here.history = [[std.time_now(), text, selected]] + here.history;
    }

    with exit {
        report selected;
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

walker drain_log {
    bot {
        take --> node::log_chunk;
    }
    log_chunk {
        report here.history;
        here.history=[];
    }
}

walker get_question_matches {
    has text, num_matches, matches;
    can use.enc_question, use.qa_score;

    with entry {matches=[];}

    bot {
        enc=use.enc_question(text);
        for i in --> {
            score=use.qa_score(enc, i.encoding);
            matches += [[score[0][0], &i]];
        }
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
            spawn here ++> node::botset;
            std.log(-->);
            disengage;
        }
    }
}

walker asim_bug_check1 {
    for i in -->:
        i.bug_check_deep['a']['b'][0]=12;
    report -->;
}

walker asim_bug_check2 {
    report -->;
}

walker asim_bug_check3 {
    for i in -->:
        i.bug_check_deep['a']['b'][0]+=12;
    report -->;
}

walker asim_bug_check4 {
    for i in -->:
        i.bug_check="testing";
    report -->;
}

walker pubinit:anyone {
    root {
        take (--> node::botset) else {
            spawn here ++> node::botset;
            std.log(-->);
            disengage;
        }
    }
}

global a = "test";

walker global_actions {
    with entry {
        report global.a;
        report global.context;
        report global.info;
        report global.info['request_context'];
        report global.b;
    }
}

walker simple {
    has anchor test_anchor = "test";
    with entry {
        report global.info['request_context']["body"];
    }
}

async walker simple_async_second_layer {
    has anchor val1, val2 = 2;
    with entry {
        report val1;
        // task2 report [1]

        report val2;
        // task2 report [1, 2]

        report global.info['request_context']["body"];
        // task2 report [1, 2, globsbody]
    }
}

async walker simple_async {
    has anchor test_anchor = "test";
    with entry {
        task1 = spawn here sync walker::simple_async_second_layer(val1 = 1);
        // report [1, 2, globsbody]

        task2 = spawn here walker::simple_async_second_layer(val1 = 1);
        // report [1, 2, globsbody]

        report task1;
        // report [ val1 = 1, val2 = 2, globsbody, anchor = 1]

        report global.info['request_context']["body"];
        // report [ val1 = 1, val2 = 2, globsbody, anchor = 1, globsbody]

        report task2;
        // report [ val1 = 1, val2 = 2, globsbody, anchor = 1, globsbody, task2 = {async_result}]
    }
}

walker simple_with_file {
    has sample, fileTypeField, binaryFile;

    can fh.attr, fh.read, fh.to_json, fh.to_base64, fh.to_bytes, fh.open;

    with entry {
        report sample;

        if fileTypeField and global.info['request_context']["body"]["ctx"]["fileTypeField"] {
            report true;
        }

        report fileTypeField[0];
        report fh.attr(fileTypeField[0]);
        report fh.read(fileTypeField[0], 0);
        report fh.to_json(fileTypeField[0]);
        report fh.to_bytes(fileTypeField[0]).str;
        report fh.to_base64(fileTypeField[0]);

        fh.open(binaryFile[0], mode = "rb");
        report fh.read(binaryFile[0], 0).str;
        report fh.to_bytes(binaryFile[0]).str;
    }
}

walker simple_custom_payload_with_file {
    has fileTypeField;

    can fh.attr, fh.read, fh.to_json, fh.to_base64, fh.to_bytes;

    with entry {
        if not fileTypeField and not global.info['request_context']["body"]["ctx"] {
            report true;
        }

        uuid = global.info['request_context']["body"]["fileTypeField"][0];
        report uuid;
        report fh.attr(uuid);
        report fh.read(uuid, 0, "r", "utf-8");
        report fh.to_json(uuid);
        report fh.to_bytes(uuid).str;
        report fh.to_base64(uuid);
    }
}

walker master_self {
    with entry {
        report jaseci.master_self(true);
    }
}