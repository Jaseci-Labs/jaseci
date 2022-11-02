walker report_clearing {
    report 5;
    report 6;
    std.clear_report();
    report 7;
}

walker internal_lib {
    internal.start_perf_test();
    report 5+3+5;
    std.clear_report();
    report internal.stop_perf_test();
}