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