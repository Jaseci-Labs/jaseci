"""
This test file is to ensure the valid syntax of jac lang.
Add new jac syntax here to test if it compile without any issue.
"""

# Import statement without trailing comma.
import:py from time {
  sleep,
  timezone,
  tzname
}


# Import statement with trailing comma.
import:py from os {
  path,
  getenv,
  getpid,
}


enum WithoutTrailComma {
    FOO = "FOO",
    BAR = "BAR"
}


enum WithTrailComma {
    FOO = "FOO",
    BAR = "BAR",
}


can without_trail_comma(a:int, b:int) {}

can with_trail_comma(
      a:int,
      b:int,
      c:int,
    ) {}


with entry {

    dict_without_trail_comma = { "key" : "value" };
    dict_with_trail_comma = {
        "key" : "val",
    };

    list_without_trail_comma = [ "foo", "bar" ];
    list_with_trail_comma = [
        "foo",
        "bar",
    ];

    set_without_trail_comma = { "foo", "bar" };
    set_with_trail_comma = {
      "foo",
      "bar",
    };

    print("Code compiled and ran successfully!");
}

