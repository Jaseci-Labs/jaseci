walker test_yield {
    has a=6;

    if(a < 10) {
        a+=1;
        report a;
        yield;
    }
    else {
        report "should start over now";
    }
}

walker test_yield_report {
    has a=6;

    if(a < 10) {
        a+=1;
        yield report a;
    }
    else {
        report "should start over now";
    }
}

walker test_yield_disengage {
    has a=6;

    if(a < 10) {
        a+=1;
        yield disengage report a;
        report "test"; #should not be printed
    }
}

walker test_yield_take {
    has a=6;

    if(a < 10) {
        a+=1;
        yield take here;
        report "test"; #should not be printed
    }
}