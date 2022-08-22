import {*} with "./ai.jac";

node bi_enc:ai_model {
    can bi_enc.train, bi_enc.infer, bi_enc.save_model;

    can train {
        train_data = file.load_json(visitor.train_file);
        bi_enc.train(
            dataset=train_data,
            from_scratch=visitor.train_from_scratch,
            training_parameters={
                "num_train_epochs": visitor.num_train_epochs
            }
        );
        if (visitor.model_name):
            bi_enc.save_model(model_path=visitor.model_name);
    }

    can infer {
        res = bi_enc.infer(
            contexts=[visitor.query],
            candidates=here.candidates,
            context_type="text",
            candidate_type="text"
        )[0];

        max_score = 0;
        max_intent = "";
        for i=0 to i<res["candidate"].length by i+=1 {
            if (res["score"][i] > max_score){
                max_intent = res["candidate"][i];
                max_score = res["score"][i];
            }
        }
        report [max_intent, max_score];
    }

    can test_model {
        eval_set = file.load_json(visitor.eval_file);
        candidates = eval_set.dict::keys;

        correct = [];
        failure = [];
        for intent in candidates {
            preds = bi_enc.infer(
                contexts=eval_set[intent],
                candidates=candidates,
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
} 