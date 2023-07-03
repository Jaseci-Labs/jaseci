walker test_kwargs {
    report rand.sentence(max_length=5, sep=".");
    report std.sort_by_col([[1,2],[3,4]], 1, true);
    report std.sort_by_col([[1,2],[3,4]], reverse=true, col_num=1);
    report std.sort_by_col([[1,2],[3,4]], col_num=1);
}

walker multistring {
    report
        "This "
        "is"
        " a multistring";
}

// # int, float, list, string, dict, bool, bytes

// walker simple {
//     has filename;

//     has anchor test_anchor: str = "test";
//     has:f myfile: bytes;
//     has nextthing: int;
//     has nextblob: bytes;

//     # Jac, needs to support binary types
//     # walker run -ctx {"test_anchor": "test", "myfile": "test.txt"}0
//     # walker run -ctx {"test_anchor": [0, "test"], "myfile": [1, "test.txt"]}
//     with entry {
//         report global.info['request_context']["body"];
//     }
// }