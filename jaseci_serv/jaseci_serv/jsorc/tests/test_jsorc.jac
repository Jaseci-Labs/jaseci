walker test_actions_tracking {
    can test_module.call;
    test_module.call("test string");
    test_module.call("test string1");
    res = test_module.call("test string2");
    report res;
}

walker test_benchmark {
    report "dummy walker";
}