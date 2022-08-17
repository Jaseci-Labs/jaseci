node model_dir;
node flair_ner {
    # load the model actions here
    can ent_ext.entity_detection, ent_ext.train;

    can train with train_and_eval_all_models entry{
        # train the model with a given dataset
        std.out("in flair ner");
        train_data = file.load_json(visitor.train_file);

        ## training model
        ent_ext.train(
            train_data = train_data,
            train_params = {
                "num_epoch": visitor.num_train_epochs.int,
                "batch_size": visitor.batch_size.int,
                "LR": visitor.learning_rate.float
                });
    }
    
    can infer with predict_entity_from_flair entry{
        # TODO: remove this
        report ent_ext.entity_detection(
            text=visitor.text,
            ner_labels=[visitor.labels]
            );
        }

    can eval with train_and_eval_all_models exit{
        # run the model against a given test set and report accuracy
        eval_data = file.load_json(visitor.eval_file);
        labels = [];
        for item in eval_data {
            for ent in item["entities"]{
                ent_label = ent["entity_type"];
                if ent_label not in labels:
                    labels.l::append(ent_label);
            }}

        total = 0;
        success = 0;
        fail = 0;
        for r in eval_data {
            ent_true = r['entities'];
            ent_pred = ent_ext.entity_detection(
                text = r["context"],
                ner_labels = labels
                );
            ent_pred = ent_pred['entities'];
            total += 1;
            status = 0;
            if ent_true.length == ent_pred.length:
                for i=0 to i<ent_true.length by i+=1:
                    if ent_true[i]["entity_type"].str::lower==ent_pred[i]["entity_value"].str::lower and
                        ent_true[i]["entity_value"].str::lower == ent_pred[i]["entity_text"].str::lower:
                        status +=1;

            if ent_true.length==status: success += 1;
            else: fail += 1;
        }
        report [{"model name":"flair_ner","data":[
            {"total":total},
            {"success":success},
            {"fail":fail},
            {"accuracy":success/total}
            ]}];
    }

    # you might also need 
    # load_model, save_model, etc.
}

node tfm_ner {
    # train,infer, eval
    can tfm_ner.extract_entity,tfm_ner.train;

    can train with train_and_eval_all_models entry{
        # train the model with a given dataset
        train_data = file.load_json(visitor.train_file);
        tfm_ner.train(
            mode = visitor.mode,
            epochs = visitor.num_train_epochs.int,
            train_data=train_data
            );
    }
    # extracting entities
    can infer with predict_entity_from_tfm entry {
        report tfm_ner.extract_entity(
            text = visitor.text
        );
    }
    # evaluate data
    can eval with train_and_eval_all_models exit{
        # run the model against a given test set and report accuracy
        eval_data = file.load_json(visitor.eval_file);
        total = 0;
        success = 0;
        fail = 0;
        for r in eval_data {
            ent_true = r['entities'];
            ent_pred = tfm_ner.extract_entity(text=r["context"]);
            total += 1;
            status = 0;
            if ent_true.length == ent_pred.length:
                for i=0 to i<ent_true.length by i+=1:
                    if ent_true[i]["entity_type"].str::lower==ent_pred[i]["entity"].str::lower and
                        ent_true[i]["entity_value"].str::lower == ent_pred[i]["text"].str::lower:
                        status +=1;

            if ent_true.length==status: success += 1;
            else: fail += 1;
        }
         report [
            {"model name":"tfm_ner","data":[
                {"total":total},
                {"success":success},
                {"fail":fail},
                {"accuracy":success/total}
                ]
                }];
    }
}

# new model
// node lstm_ner {
// }

edge ner_model {
    has model_type;
}

graph ner_eval_graph {
    has anchor ner_model_dir;
    spawn {
        ner_model_dir = spawn node::model_dir;
        flair_ner_node = spawn node::flair_ner;
        tfm_ner_node = spawn node::tfm_ner;

        ner_model_dir -[ner_model(model_type="flair_ner")]-> flair_ner_node;
        ner_model_dir -[ner_model(model_type="tfm_ner")]-> tfm_ner_node;
    }
}


walker init {
    root {
       spawn here --> graph::ner_eval_graph; 
    }
}

## creating walker 
walker train_and_eval_all_models {
    # Take in a training and eval dataset
    has train_file;
    has eval_file;
    has num_train_epochs;
    has batch_size;
    has learning_rate;
    has mode;

    # Train all NER models on the train set
    # and evaluate them on the eval set
    # report accuracy performance across all NER models
    root {
        take --> node::model_dir;
    }
    model_dir {
        take -->;
    }
}

walker predict_entity_from_tfm{
    has text;

    root {
        take --> node::model_dir;
    }
    model_dir {
        take -->;
    }
}

walker predict_entity_from_flair{
    has text;
    has labels;

    root {
        take --> node::model_dir;
    }
    model_dir {
        take -->;
    }
}