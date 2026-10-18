import from "motion/react" { motion }

glob MPath: any = motion.path,
     MLine: any = motion.line,
     MText: any = motion.text,
     C_COMPILER: str = "#a78bfa",
     C_PROGRAM: str = "#ff6b35",
     C_ECO: str = "#56d364";

def:pub StackBox(x: int, y: int, label: str, sub: str) -> JsxElement;

def:pub GhostChip(x: int, y: int, w: int, label: str) -> JsxElement;

def:pub ToolChip(x: int, y: int, w: int, label: str, tone: str = "") -> JsxElement;

def:pub RoleDot(color: str, label: str) -> JsxElement;

def:pub CallPill(cx: int, label: str) -> JsxElement;

def:pub Boundary(y: int, label: str) -> JsxElement;

def:pub SynechicDiagram -> JsxElement;
