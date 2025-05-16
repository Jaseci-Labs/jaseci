from jaclang.compiler.jtyping import JType
from jaclang.compiler.jtyping.constraint import JTypeConstraint  # assuming it's in a separate file


class JTypeConstraintSolver:
    def __init__(self):
        self.constraints: list[JTypeConstraint] = []
        self.substitutions: dict[str, JType] = {}  # Map from JTypeVar.name → resolved JType

    def add_constraint(self, left: JType, right: JType, source_node: Optional[UniNode] = None):
        self.constraints.append(JTypeConstraint(left=left, right=right, source_node=source_node))

    def solve(self):
        for constraint in self.constraints:
            try:
                self._unify(constraint.left, constraint.right)
            except TypeError as e:
                loc = constraint.source_node.loc if constraint.source_node else "unknown location"
                print(f"Type Error at {loc}: {e}")

    def _unify(self, t1: JType, t2: JType):
        # Resolve variables if already substituted
        t1 = self._resolve(t1)
        t2 = self._resolve(t2)

        # Case 1: They are the same already
        if t1 == t2:
            return

        # Case 2: One is a type variable
        if isinstance(t1, JTypeVar):
            self.substitutions[t1.name] = t2
        elif isinstance(t2, JTypeVar):
            self.substitutions[t2.name] = t1
        elif is_subtype(t1, t2):
            return
        else:
            raise TypeError(f"Cannot unify {t1} with {t2}")

    def _resolve(self, t: JType) -> JType:
        while isinstance(t, JTypeVar) and t.name in self.substitutions:
            t = self.substitutions[t.name]
        return t

    def get_final_type(self, t: JType) -> JType:
        return self._resolve(t)

    def get_type_var_mapping(self) -> dict[str, JType]:
        return {k: self._resolve(v) for k, v in self.substitutions.items()}
