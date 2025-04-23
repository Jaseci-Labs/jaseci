import re
from pathlib import Path

MARGIN = 0.10
CURRENT = "jac/.performance/durations_current.txt"
BASELINE = "jac/.performance/durations_baseline.txt"


def parse_durations(path: str) -> dict:
    text = Path(path).read_text()
    pattern = re.compile(r"([\d\.]+)s\s+call\s+(\S+)")
    durations = {}
    for match in pattern.finditer(text):
        duration = float(match.group(1))
        test_name = match.group(2)
        durations[test_name] = duration
    return durations


def compare(current: dict, baseline: dict) -> list:
    regressions = []
    for test, curr in current.items():
        if test in baseline:
            allowed = baseline[test] * (1 + MARGIN)
            if curr > allowed and curr > 10:
                regressions.append((test, baseline[test], curr))
    return regressions


if __name__ == "__main__":
    print(__file__)
    curr_dur = parse_durations(CURRENT)
    try:
        base_dur = parse_durations(BASELINE)
    except FileNotFoundError:
        print("⚠️  No baseline found. Skipping check.")
        exit(0)

    regressed = compare(curr_dur, base_dur)
    if regressed:
        print("❌ Performance issues detected:")
        for test, old, new in regressed:
            print(f"    {test}: {old:.2f}s → {new:.2f}s")
        exit(1)
    else:
        print("✅  No performance regressions.")
