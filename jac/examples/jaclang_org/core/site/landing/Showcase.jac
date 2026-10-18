import from "@jac/runtime" { Link }
import from "@hugeicons/react" { HugeiconsIcon }
import from "@hugeicons/core-free-icons" { CheckmarkCircle01Icon, ArrowUpRight01Icon }

glob _NATIVE_LINES: list[str] = [
         "obj Buffer { has n: int = 0; }",
         "",
         "with entry {",
         "    a: own Buffer = Buffer();   # opt in, one declaration",
         "    v: &Buffer = &a;            # shared borrow of the owner",
         "    a.n = 5;    # error[E1303]: cannot mutate while borrowed",
         "    print(v.n); # the borrow remains live through this use",
         "    b = a;      # moves the value out of 'a'",
         "    print(a);   # error[E1301]: use of 'a' after move",
         "}",
         "",
         "# jac build --as native  →  zero-RC machine code",

     ];

def:pub ShowcasePanel(
    lines: list[str],
    file: str,
    heading: str,
    blurb: str,
    points: list[str],
    link_label: str,
    link_href: str
) -> JsxElement;

def:pub Showcase -> JsxElement;
