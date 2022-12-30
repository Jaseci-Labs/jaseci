node faq_root:cai_state {
  can use.qa_classify;
    can nlu {
      if (!visitor.wlk_ctx["prev_state"]) {
        answers = -->.answer;
        best_answer = use.qa_classify(
          text = visitor.question,
          classes = answers
        );
        visitor.wlk_ctx["intent"] = best_answer["match"];
      }
    }
    can process {
      if (visitor.wlk_ctx["prev_state"]): visitor.wlk_ctx["respond"] = true;
      else {
        for n in --> {
          if (n.context["answer"] == visitor.wlk_ctx["intent"]){
            visitor.wlk_ctx["next_state"] = n;
            break;
          }
        }
        visitor.wlk_ctx["prev_state"] = here;
      }
    }
    can nlg {
      visitor.response = "I can answer a variety of FAQs related to Tesla. What can I help you with?";
    }
}

node faq_state:cai_state {
  has question;
  has answer;
  can nlg {
    visitor.response = here.answer;
  }
}

walker init {
  root {
    spawn here --> node::faq_root;
    spawn here walker::ingest_faq(kb_file="./tesla_faq.json");
    spawn here walker::ask;
  }
}

walker ask {
    can use.qa_classify;
    has question;
    root {
        question = std.input(">");
        take --> node::faq_root;
    }
    faq_root {
        answers = -->.answer;
        best_answer = use.qa_classify(
            text = question,
            classes = answers
        );
        take --> node::faq_state(answer==best_answer["match"]);
    }
    faq_state {
        std.out(here.answer);
    }
}

walker ingest_faq {
    has kb_file;
    root: take --> node::faq_root;
    faq_root {
        kb = file.load_json(kb_file);
        for faq in kb {
            answer = faq["answer"];
            spawn here --> node::faq_state(answer=answer);
        }
    }
}
