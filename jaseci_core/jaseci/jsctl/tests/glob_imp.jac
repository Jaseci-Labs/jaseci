global say = "resetting year to 1995:";

walker cust_report{
    report:custom = {'a': 'b'};
}

walker cust_report_neutralize{
    report:custom = {'a': 'b'};
    report:custom = null;
}

walker disengage_report{
    disengage report:custom = {'a': 'b'};
}