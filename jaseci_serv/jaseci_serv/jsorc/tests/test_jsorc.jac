walker test_actions_tracking {
    can example_module.call;
    example_module.call("test string");
    example_module.call("test string1");
    res = example_module.call("test string2");
    report res;
}

walker test_benchmark {
    report "dummy walker";
}