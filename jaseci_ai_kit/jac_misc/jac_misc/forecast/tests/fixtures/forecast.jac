walker test_preprocess{
    can forecast.preprocess;
    variables = {'variable1': [3, 2, 1, 0, 5, 6, 9], 'variable2': [4, 5, 6, 8, 5, 7, 8]};
    times = ['2022-05-01', '2022-05-02', '2022-05-03', '2022-05-04', '2022-05-05', '2022-05-06', '2022-05-07'];
    report forecast.preprocess(times,variables);
}

walker test_split{
    can forecast.split;
    can forecast.preprocess;

    variables = {'variable1': [3, 2, 1, 0, 5, 6, 9]};
    times = ['2022-05-01', '2022-05-02', '2022-05-03', '2022-05-04', '2022-05-05', '2022-05-06', '2022-05-07'];
    cuttoff = '2022-05-03';

    forecast.preprocess(times,variables);
    report forecast.split(cuttoff,"True");
}

walker test_scale{
    can forecast.scale;
    can forecast.preprocess;

    variables = {'variable1': [3, 2, 1, 0, 5, 6, 9], 'variable2': [4, 5, 6, 8, 5, 7, 8]};
    times = ['2022-05-01', '2022-05-02', '2022-05-03', '2022-05-04', '2022-05-05', '2022-05-06', '2022-05-07'];
    forecast.preprocess(times,variables);

    report forecast.scale();
}

walker test_create_model{
    can forecast.create_model;
    has params_dict = {"input_chunk": 4, "output_chunk":1, "hidden_size":64, "quantiles":[0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99]};

    report forecast.create_model("transformer", params_dict);
}

walker test_train{
    can forecast.preprocess;
    can forecast.split;
    can forecast.create_model;
    can forecast.train;

    has covariate1 = "year";
    has covariate2 = "month";
    has params_dict = {"input_chunk": 4, "output_chunk":1, "hidden_size":64, "quantiles":[0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99]};
    has variables = {'variable1': [3, 2, 1, 0, 5, 6, 9], 'variable2': [4, 5, 6, 8, 5, 7, 8]};
    has times = ['2022-05-01', '2022-05-02', '2022-05-03', '2022-05-04', '2022-05-05', '2022-05-06', '2022-05-07'];
    cuttoff = '2022-05-06';

    forecast.preprocess(times,variables);
    forecast.split(cuttoff,"True");
    forecast.create_model("transformer", params_dict);

    report forecast.train(covariate1,covariate2);
}


walker test_evaluate{
    can forecast.preprocess;
    can forecast.split;
    can forecast.create_model;
    can forecast.train;
    can forecast.evaluate;

    has covariate1 = "year";
    has covariate2 = "month";
    has params_dict = {"input_chunk": 4, "output_chunk":1, "hidden_size":64, "quantiles":[0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99]};
    has variables = {'variable1':[0.5, 0.6, 0.8, 1.1, 1.5, 2.1, 2.1, 2.2, 1.9, 1.8]};
    has times = ['2022-05-01', '2022-05-02', '2022-05-03', '2022-05-04', '2022-05-05', '2022-05-06', '2022-05-07', '2022-05-08', '2022-05-09', '2022-05-10'];
    cuttoff = '2022-05-06';

    forecast.preprocess(times,variables);
    forecast.split(cuttoff,"True");
    forecast.create_model("transformer", params_dict);

    forecast.train(covariate1,covariate2);
    report forecast.evaluate(2);
}

walker test_predict{
    can forecast.preprocess;
    can forecast.split;
    can forecast.create_model;
    can forecast.train;
    can forecast.predict;

    has covariate1 = "year";
    has covariate2 = "month";
    has params_dict = {"input_chunk": 4, "output_chunk":1, "hidden_size":64, "quantiles":[0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99]};
    has variables = {'variable1':[0.5, 0.6, 0.8, 1.1, 1.5, 2.1, 2.1, 2.2, 1.9, 1.8]};
    has times = ['2022-05-01', '2022-05-02', '2022-05-03', '2022-05-04', '2022-05-05', '2022-05-06', '2022-05-07', '2022-05-08', '2022-05-09', '2022-05-10'];
    cuttoff = '2022-05-06';

    forecast.preprocess(times,variables);
    forecast.split(cuttoff,"True");
    forecast.create_model("transformer", params_dict);

    forecast.train(covariate1,covariate2);
    report forecast.predict(2);
}