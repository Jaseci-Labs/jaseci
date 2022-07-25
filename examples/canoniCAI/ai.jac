walker train_and_eval_model {
    has train_file = "data/clf_train.json";
}

node ai {
    can train_and_eval with train_and_eval_model entry {
        if(visitor.train_file.length > 1){
            if(file.load_json(visitor.train_file)){
                dataset = file.load_json(visitor.train_file);
            }
        }
    }
}

node classifier:ai{
    can train_and_eval with train_and_eval_model entry {
        ::ai:train_and_eval;
        here::infer;
    }

    can infer {

    }
}