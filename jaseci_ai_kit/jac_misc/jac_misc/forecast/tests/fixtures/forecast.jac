walker test_preprocess{
    can forecast.preprocess;
    variables = {'variable1': [3, 2, 1, 0], 'variable2': [4, 5, 6, 8]}
    times = ['2022-12-05','2022-12-12','2022-12-19','2022-12-26']
    report forecast.preprocess(times,variables)
}