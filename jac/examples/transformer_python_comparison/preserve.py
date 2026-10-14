"""Hash existing example/library trees without importing or modifying them."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
# A later, separately authorized comparison example is not part of this baseline.
NEW_EXAMPLES = (HERE, HERE.parent / "graph_frontend_comparison")


def snapshot():
    report = {}
    for relative in ('jac/examples', 'jac/jaclang/lib'):
        root = REPO / relative
        rows = []
        for path in sorted(root.rglob('*')):
            if not path.is_file() or any(path.is_relative_to(folder) for folder in NEW_EXAMPLES):
                continue
            rows.append(str(path.relative_to(root)) + '\0' + hashlib.sha256(path.read_bytes()).hexdigest())
        report[relative] = dict(files=len(rows), sha256=hashlib.sha256('\n'.join(rows).encode()).hexdigest())
    return report


def check():
    actual = snapshot()
    assert actual == json.loads((HERE / 'preservation.json').read_text()), 'Existing examples/libraries changed'
    return actual


if __name__ == '__main__':
    path = HERE / 'preservation.json'
    if path.exists():
        print(json.dumps(check(), indent=2))
    else:
        path.write_text(json.dumps(snapshot(), indent=2) + '\n')
