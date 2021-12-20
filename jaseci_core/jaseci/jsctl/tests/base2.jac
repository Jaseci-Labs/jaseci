import {walker*} with "jaseci/jsctl/tests/import.jac";

node person {
    has name;
    has byear;
    can set_year with setter entry {
        byear = visitor.year;
    }
    can print_out with exit {
        report [byear, " from ", visitor.info];
    }
    can reset {  # <-- Could add 'with activity' for equivalent behavior
        byear = "1995-01-01";
        report ["resetting year to 1995:", here.context];
    }
}
