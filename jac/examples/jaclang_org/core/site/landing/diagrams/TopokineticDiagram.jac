import from "motion/react" { motion }

glob MLine: any = motion.line,
     MCircle: any = motion.circle,
     _GNODES: list[dict[str, any]] = [
         {"x": 150, "y": 92},
         {"x": 150, "y": 228},
         {"x": 252, "y": 62},
         {"x": 252, "y": 160},
         {"x": 252, "y": 258},
         {"x": 352, "y": 112},
         {"x": 352, "y": 208},

     ],
     _GEDGES: list[dict[str, any]] = [
         {"x1": 70, "y1": 160, "x2": 150, "y2": 92},
         {"x1": 70, "y1": 160, "x2": 150, "y2": 228},
         {"x1": 150, "y1": 92, "x2": 252, "y2": 62},
         {"x1": 150, "y1": 92, "x2": 252, "y2": 160},
         {"x1": 150, "y1": 228, "x2": 252, "y2": 160},
         {"x1": 150, "y1": 228, "x2": 252, "y2": 258},
         {"x1": 252, "y1": 62, "x2": 352, "y2": 112},
         {"x1": 252, "y1": 160, "x2": 352, "y2": 112},
         {"x1": 252, "y1": 160, "x2": 352, "y2": 208},
         {"x1": 252, "y1": 258, "x2": 352, "y2": 208},

     ];

def:pub TopokineticDiagram -> JsxElement;

def:pub GhostNote(x: int, y: int, label: str) -> JsxElement;
