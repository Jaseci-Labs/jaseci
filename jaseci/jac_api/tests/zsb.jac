node botset;
node bot { has anchor name; }
node answer { has text, encoding; }


walker get_bots {
    root { take --> node::botset; }
    botset { report -->; disengage; }
}

walker add_bot {
    has name;
    root { take --> node::botset; }
    botset {
        bot=spawn here --> node::bot(name=name);
        report bot;
        disengage;
    }
}

walker get_answers {
    bot {
        report -->;
        disengage;
    }
}

walker create_answer {
    has text;
    can use.enc_answer;

    bot {
        ans = spawn here --> node::answer(text=text);
        ans.encoding = use.enc_answer(text);
        std.log(ans);
        report ans;
        std.log("again: ",ans);
        disengage;
    }
}

walker ask_question {
    has text;
    can use.enc_question, use.qa_score;

    bot {
        enc=use.enc_question(text);
        selected = false;
        max_score = 0;
        for i in --> {
            score=use.qa_score();
            if(score[0][0]>max_score){
                selected = i;
                max_score=score[0][0];
            }
        }
        report selected;
        disengage;
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
