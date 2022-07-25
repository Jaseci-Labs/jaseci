import {*} with "./ai.jac";

node biencoder:classifier {
    has pretrained = {
        "tinybert": "prajjwal1/bert-tiny",
        "distillbert": "distilbert-base-uncased"
    };
    has candidates;
    can bi_enc.train, bi_enc.infer, bi_enc.load_model, bi_enc.save_model, bi_enc.set_model_config;

    can load_model with init entry {
        if (visitor.load_model and "biencoder" in visitor.models_to_load) {
            bi_enc.load_model(visitor.models_to_load["biencoder"]);
        }
    }

    can set_candidates with set_biencoder_candidates entry {
        train_data = file.load_json(visitor.train_file);
        here.candidates = train_data.d::keys;
    }

    can train_model with train_biencoder activity {
        # load the data from file
        train_data = file.load_json(visitor.train_file);
        here.candidates = train_data.d::keys;
        bi_enc.train(
            dataset=train_data,
            from_scratch=visitor.train_from_scratch,
            training_parameters={
                "num_train_epochs": visitor.num_train_epochs
            }
        );
    }

    can save_model with save_biencoder entry {
        bi_enc.save_model(model_path=visitor.model_name);
    }

    can set_pretrained_model with set_biencoder_pretrained_model entry {
        bi_enc.set_model_config({
            "model_name": here.pretrained[visitor.model_type]
        });
    }

    can infer with infer_biencoder entry {
        res = bi_enc.infer(
            contexts=[visitor.query],
            candidates=here.candidates,
            context_type="text",
            candidate_type="text"
        )[0];
        # Sort result
        max_score = 0;
        max_intent = "";
        for i=0 to i<res["candidate"].length by i+=1 {
            if (res["score"][i] > max_score){
                max_intent = res["candidate"][i];
                max_score = res["score"][i];
            }
        }
        report [max_intent, max_score];
        report res;
    }

    can train_and_eval with train_and_eval_biencoder entry {
        dataset = file.load_json(visitor.train_file);
        train_set = {};
        eval_set = {};

        here.candidates = [];
        for intent in dataset.dict::keys {
            here.candidates.l::append(intent);
            total_sent = dataset[intent].length;
            train_set[intent] = [];
            eval_set[intent] = [];
            for sent in dataset[intent] {
                draw = rand.integer(0, 9);
                if (draw == 0) {
                    eval_set[intent].l::append(sent);
                }else{
                    train_set[intent].l::append(sent);
                }
            }
        }

        bi_enc.train(
            dataset=train_set,
            from_scratch=true,
            training_parameters={
                "num_train_epochs": visitor.num_train_epochs
            }
        );

        correct = [];
        failure = [];
        for intent in eval_set.dict::keys {
            preds = bi_enc.infer(
                contexts=eval_set[intent],
                candidates=here.candidates,
                context_type="text",
                candidate_type="text"
            );
            for i=0 to i<preds.length by i+=1 {
                pred = preds[i];
                max_score = 0;
                max_intent = "";
                for j=0 to j<pred["candidate"].length by j+=1 {
                    if (pred["score"][j] > max_score){
                        max_intent = pred["candidate"][j];
                        max_score = pred["score"][j];
                    }
                }
                if (intent == max_intent): correct.l::append(eval_set[intent][i]);
                else {
                    failure.l::append({
                        "sent": eval_set[intent][i],
                        "ground truth": intent,
                        "prediction": max_intent
                    });
                }
            }
        }
        report {
            "accuracy": correct.length/(correct.length+failure.length),
            "correct": correct.length,
            "failure": failure.length,
            "failed_sents": failure
        };
    }

    can run_test with test_biencoder entry {
        test_data = file.load_json(visitor.test_file);
        correct = [];
        failure = [];
        cands = test_data.dict::keys;
        for intent in test_data.dict::keys {
            preds = bi_enc.infer(
                contexts=test_data[intent],
                candidates=cands,
                context_type="text",
                candidate_type="text"
            );
            for i=0 to i<preds.length by i+=1 {
                pred = preds[i];
                max_score = 0;
                max_intent = "";
                for j=0 to j<pred["candidate"].length by j+=1 {
                    if (pred["score"][j] > max_score){
                        max_intent = pred["candidate"][j];
                        max_score = pred["score"][j];
                    }
                }
                if (intent == max_intent): correct.l::append(test_data[intent][i]);
                else {
                    failure.l::append({
                        "sent": test_data[intent][i],
                        "ground truth": intent,
                        "prediction": max_intent
                    });
                }
            }
        }
        report {
            "accuracy": correct.length/(correct.length+failure.length),
            "correct": correct.length,
            "failure": failure.length,
            "failed_sents": failure
        };
    }
}

walker train_biencoder {
    has train_file = "data/clf_train.json";
    has num_train_epochs = 50;
    has from_scratch = false;
    has balance_intents = false;
    std.out("in train_biencoder");
    root: take --> node::cai_root;
    cai_root {
        take --> node::biencoder;
    }
    biencoder {
        here::train_model;
    }
}

walker set_biencoder_pretrained_model {
    has model_type;
    root: take --> node::cai_root;
    cai_root: take --> node::biencoder;
}

walker save_biencoder {
    has model_name;
    root: take --> node::cai_root;
    cai_root: take --> node::biencoder;
}

walker infer_biencoder {
    has query;
    root: take --> node::cai_root;
    cai_root: take --> node::biencoder;
}

walker set_biencoder_candidates {
    has train_file = "data/clf_train.json";
    root: take --> node::cai_root;
    cai_root: take --> node::biencoder;
}

walker train_and_eval_biencoder {
    has train_file = "data/clf_train.json";
    has num_train_epochs = 20;
    root: take --> node::cai_root;
    cai_root: take --> node::biencoder;
}

walker test_biencoder {
    has test_file = "data/clf_test.json";
    root: take --> node::cai_root;
    cai_root: take --> node::biencoder;
}