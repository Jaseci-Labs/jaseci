walker test_create_head_list {
    can ph.create_head_list;
    ph.create_head_list(config_file = 'jaseci_ai_kit/modules/ph/tests/fixtures/config.yaml');
}

walker test_create_head{
    can ph.create_head;
    report ph.create_head(uuid = 'test_head');
}

walker test_predict {
    can ph.predict;
    report ph.predict(uuid = 'test_head', data = 'Where is the nearest coffee shop?');
}

walker test_train {
    can ph.train_head;
    ph.train_head(uuid = 'test_head', config_file = 'jaseci_ai_kit/modules/ph/tests/fixtures/config.yaml');
}

walker test_load_weights {
    can ph.load_weights;
    ph.load_weights(uuid = 'test_head', path = 'output/models/PersonalizedHeadTrainer/test_head/model_best.pth');
}

walker test_predict_trained {
    can ph.predict;
    report ph.predict(uuid = 'test_head', data = 'Where is the nearest coffee shop?');
}