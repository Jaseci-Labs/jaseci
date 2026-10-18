import from "motion/react" { motion }

glob MPath: any = motion.path,
     _IN_PATHS: list[str] = [
         "M124,65 C230,65 300,118 384,140",
         "M124,150 L384,150",
         "M124,235 C230,235 300,182 384,160",

     ],
     _OUT_PATHS: list[str] = [
         "M496,140 C580,118 650,65 756,65",
         "M496,150 L756,150",
         "M496,160 C580,182 650,235 756,235",

     ],
     _INS: list[dict[str, any]] = [
         {"y": 52, "label": "PyPI"},
         {"y": 137, "label": "npm"},
         {"y": 222, "label": "C ABI"},

     ],
     _OUTS: list[dict[str, any]] = [
         {"y": 52, "label": "Python bytecode"},
         {"y": 137, "label": "JavaScript"},
         {"y": 222, "label": "native · wasm"},

     ];

def:pub PolypilerDiagram -> JsxElement;
