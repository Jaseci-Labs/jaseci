walker test_create_head_list {
    can ph.create_head_list;
    ph.create_head_list({
        "Model":{
            "args":{
                "batch_first": true,
                "embedding_length": 768
            }
        }
    });
}

walker test_create_head{
    can ph.create_head;
    report ph.create_head('test_head');
}

walker test_predict {
    can ph.predict;
    report ph.predict(uuid = 'test_head', data = 'Where is the nearest coffee shop?');
}

walker test_train {
    can ph.train_head;
    ph.train_head('test_head', {
        "Trainer":{
            "trainer":{
                "epochs": 3
            }
        }
    });
}

walker test_predict_trained {
    can ph.predict;
    report ph.predict(uuid = 'test_head', data = 'Where is the nearest coffee shop?');
}