import from "@hugeicons/react" { HugeiconsIcon }
import from "@hugeicons/core-free-icons" { ChampionIcon }

glob SUBSTANCE_ROWS: list[list[str]] = [
         [
             "Jac volume",
             "18",
             "Jac lines on a log scale — full marks near 50k lines, so a 500-line gem still registers"
         ],
         [
             "Jac share of the code",
             "12",
             "the percentage of the repo's programming-language bytes that are Jac. Markup, styles, shell, and config (.html/.css/.sh/.json/...) don't count as code, and vendored dirs (node_modules, .venv, dist, ...) never dilute the share — a thin Jac wrapper around a Python codebase can't pass as substance"
         ]
     ],
     BREADTH_ROWS: list[list[str]] = [
         [
             "Object-spatial programming",
             "7",
             "walker / node / edge declarations, spawn, ++> connect ops"
         ],
         ["AI integration", "6", "delegating work with `by llm`"],
         ["Client codespace", "5", "JSX components: JsxElement / JsxPage returns"],
         [
             "Server codespace",
             "4",
             ".sv.jac files, sv blocks, walker:pub / def:pub endpoints"
         ],
         ["Native codespace", "4", ".na.jac files, na blocks or na imports"],
         ["Tests", "3", "test blocks"],
         ["Multi-codespace bonus", "3", "using two or more of cl / sv / na together"]
     ],
     CRAFT_ROWS: list[list[str]] = [
         [
             "README",
             "2 + 3",
             "2 for having one, up to 3 more scaling with length (full near 60 lines)"
         ],
         ["jac.toml", "4", "packaged as a Jac project"],
         ["License", "3", "LICENSE / LICENSE.md / LICENSE.txt"],
         ["CI", "3", "any workflow under .github/workflows/"],
         ["docs/", "2", "a docs directory"],
         ["Recent upkeep", "3 / 2 / 1", "last push within 30 / 90 / 365 days"]
     ],
     COMMUNITY_ROWS: list[list[str]] = [
         ["Stars", "12", "log scale, full marks near 1,000 stars"],
         ["Forks", "5", "log scale, full marks near 200 forks"],
         ["Topics", "3", "at least one GitHub topic is set"]
     ],
     BELT_STEPS: list[list[str]] = [
         ["white", "0"],
         ["yellow", "20"],
         ["orange", "35"],
         ["green", "50"],
         ["brown", "65"],
         ["black", "80"]
     ];

def:pub RubricTable(cols: list[str], rows: list[list[str]]) -> JsxElement;

def:pub Section(title: str, total: str, blurb: str) -> JsxElement;

def:pub Methodology -> JsxElement;
