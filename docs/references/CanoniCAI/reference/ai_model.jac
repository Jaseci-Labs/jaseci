node bi_enc {
    can bi_enc.train, bi_enc.infer;

    can train {
        train_data = file.load_json(visitor.train_file);
        bi_enc.train(
            dataset=train_data,
            from_scratch=visitor.from_scratch,
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
            candidates=visitor.labels,
            context_type="text",
            candidate_type="text"
        )[0];
        visitor.prediction = res["predicted"];
    }
}

node tfm_ner {
    can tfm_ner.train, tfm_ner.extract_entity;

    can train {
        train_data = file.load_json(visitor.train_file);
        tfm_ner.train(
            mode = "default",
            epochs = visitor.num_train_epochs,
            train_data = train_data,
            val_data = train_data
        );
    }

    can infer {
        res = tfm_ner.extract_entity(
            text = visitor.query
        );
        visitor.prediction = res;
    }
}

walker train {
    has train_file, model_type;
    has num_train_epochs = 50, from_scratch = true, model_name = "";
    root {
        if (model_type == "bi_enc") {
            take --> node::bi_enc else {
                spawn here ++> node::bi_enc;
                take --> node::bi_enc;
            }
        }
        elif (model_type == "tfm_ner") {
            take --> node::tfm_ner else {
                spawn here ++> node::tfm_ner;
                take --> node::tfm_ner;
            }
        } else {
            std.err("Unrecongized model type.");
        }
    }
    bi_enc, tfm_ner: here::train;
}

walker infer {
    has query, model_type, interactive = true;
    has labels, prediction;
    root {
        if (model_type == "bi_enc") {
            take --> node::bi_enc else {
                spawn here ++> node::bi_enc;
                take --> node::bi_enc;
            }
        }
        elif (model_type == "tfm_ner") {
            take --> node::tfm_ner else {
                spawn here ++> node::tfm_ner;
                take --> node::tfm_ner;
            }
        } else {
            std.err("Unrecongized model type.");
        }
    }
    bi_enc, tfm_ner {
        if (interactive) {
            while true {
                query = std.input("Enter input text (Ctrl-C to exit)> ");
                here::infer;
                std.out(prediction);
            }
        } else {
            here::infer;
            report prediction;
        }
    }
}

walker save_model {
    has model_path, model_type;
    can bi_enc.save_model, tfm_ner.save_model;
    if (model_type == "bi_enc") {
        bi_enc.save_model(model_path);
    } elif (model_type == "tfm_ner") {
        tfm_ner.save_model(model_path=model_path);
    } else {
        std.err("Unrecongized model type.");
    }
}

walker load_model {
    has model_path, model_type;
    can bi_enc.load_model, tfm_ner.load_model;
    if (model_type == "bi_enc") {
        bi_enc.load_model(model_path);
    } elif (model_type == "tfm_ner") {
        tfm_ner.load_model(model_path=model_path);
    } else {
        std.err("Unrecongized model type.");
    }
}
