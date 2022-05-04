import {walker::setter, walker::init} with "./import.jac";
import {global::say} with "./import.jac";

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
        report [global.say, here.context];
    }
}
