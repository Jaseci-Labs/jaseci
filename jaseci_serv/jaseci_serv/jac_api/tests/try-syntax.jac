

walker walker_exception_no_try_else {
    can request.get;
    with entry {
        request.get("invalidUrl");
    }
}

walker walker_exception_with_try_else {
    can request.get;
    with entry {
        try {
            request.get("invalidUrl");
        } else with error {
            report error;
            report:error = error;
        }
    }
}

walker walker_exception_with_try_else_multiple_line {
    can request.get;
    with entry {
        try {
            std.log("######");
            std.log("######");


            std.log("######");

            request.get("invalidUrl", {}, {});

            std.log("######");
            std.log("######");
            std.log("######");
        } else with error {
            report error;
            report:error = error;
        }
    }
}