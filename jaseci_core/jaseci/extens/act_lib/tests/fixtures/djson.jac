walker parser {
    can djson.parse;
    with entry {

        report "[1]: whole source";
        report djson.parse(
            {"a": 1},
            {"b": "{{$}}"}
        );

        report "[2]: whole source cast to string";
        report djson.parse(
            {"a": 1},
            {"b": "{{$s}}"}
        );

        report "[3]: int";
        report djson.parse(
            {"a": 1},
            {"b": "{{$.a}}"}
        );

        report "[4]: int cast to string";
        report djson.parse(
            {"a": 1},
            {"b": "{{$s.a}}"}
        );

        report "[5]: int partial";
        report djson.parse({"a": 1},
            {"b": "partial-{{$.a}}"}
        );

        report "[6]: string";
        report djson.parse(
            {"a": "1"},
            {"b": "{{$.a}}"}
        );

        report "[7]: string partial";
        report djson.parse(
            {"a": "1"},
            {"b": "partial-{{$.a}}"}
        );

        report "[8]: int list";
        report djson.parse(
            {"a": [1]},
            {"b": "{{$.a}}"}
        );

        report "[9]: int list cast to string";
        report djson.parse(
            {"a": [1]},
            {"b": "{{$s.a}}"}
        );

        report "[10]: int list partial";
        report djson.parse(
            {"a": [1]},
            {"b": "partial-{{$.a}}"}
        );

        report "[11]: int list index";
        report djson.parse(
            {"a": [1]},
            {"b": "{{$.a.0}}"}
        );

        report "[12]: string list";
        report djson.parse(
            {"a": ["1"]},
            {"b": "{{$.a}}"}
        );

        report "[13]: string list cast to string";
        report djson.parse(
            {"a": ["1"]},
            {"b": "{{$s.a}}"}
        );

        report "[14]: string list partial";
        report djson.parse(
            {"a": ["1"]},
            {"b": "partial-{{$.a}}"}
        );

        report "[15]: string list index";
        report djson.parse(
            {"a": ["1"]},
            {"b": "{{$.a.0}}"}
        );

        report "[16]: dict";
        report djson.parse(
            {"a": {"test": 1}},
            {"b": "{{$.a}}"}
        );

        report "[17]: dict cast to string";
        report djson.parse(
            {"a": {"test": 1}},
            {"b": "{{$s.a}}"}
        );

        report "[18]: dict partial";
        report djson.parse(
            {"a": {"test": 1}},
            {"b": "partial-{{$.a}}"}
        );

        report "[19]: nested dict";
        report djson.parse(
            {"a": {"test": 1}},
            {"b": "{{$.a.test}}"}
        );

        report "[20]: nested dict cast to string";
        report djson.parse(
            {"a": {"test": 1}},
            {"b": "{{$s.a.test}}"}
        );

        report "[21]: nested dict partial";
        report djson.parse(
            {"a": {"test": 1}},
            {"b": "partial-{{$.a.test}}"}
        );

        report "[22]: super nested dict that returns the value";
        report djson.parse(
            {"a": {"test": [{
                "a":1,
                "b":2,
                "c":3
            }]}},
            "{{$.a.test.0.c}}"
        );

        report "[23]: string target";
        report djson.parse(
            {"a": "1"},
            "{{$.a}}"
        );

        report "[24]: string target";
        report djson.parse(
            {"a": "1"},
            "{{$.a}}"
        );

        report "[25]: string target partial";
        report djson.parse(
            {"a": "1"},
            "partial-{{$.a}}"
        );

        report "[26]: string source";
        report djson.parse(
            "testing",
            {"b": "{{$}}"}
        );

        report "[27]: string source partial";
        report djson.parse(
            "testing",
            {"b": "partial-{{$}}"}
        );

        report "[28]: int source";
        report djson.parse(
            1,
            {"b": "{{$}}"}
        );

        report "[29]: int source cast";
        report djson.parse(
            1,
            {"b": "{{$s}}"}
        );

        report "[30]: int source partial";
        report djson.parse(
            1,
            {"b": "partial-{{$}}"}
        );

        report "[31]: int source string target";
        report djson.parse(
            1,
            "{{$}}"
        );

        report "[32]: int source string target cast";
        report djson.parse(
            1,
            "{{$s}}"
        );

        report "[33]: not existing";
        report djson.parse(
            {"a": {"b": 1}},
            {"b": "{{$.a.c}}"}
        );

        report "[34]: not existing cast to string empty";
        report djson.parse(
            {"a": {"b": 1}},
            {"b": "{{$s.a.c}}"}
        );

        report "[35]: string source cast to dict";
        report djson.parse(
            "{}",
            "{{$d}}"
        );

        report "[36]: string source cast to int";
        report djson.parse(
            "1",
            "{{$i}}"
        );
    }
}