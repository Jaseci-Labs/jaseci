import from "motion/react" { motion }

glob MPath: any = motion.path,
     MLine: any = motion.line,
     MText: any = motion.text,
     MCircle: any = motion.circle;

def:pub TaxChip(x: int, y: int, w: int, label: str) -> JsxElement;

def:pub GradualBorrowDiagram -> JsxElement;
