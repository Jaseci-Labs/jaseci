import subprocess
import argparse
import os


def get_all_tests(filter_str: str):
    tests = []
    for root, _, files in os.walk(os.getcwd()):
        for file in files:
            if file.startswith(filter_str) and file.endswith(".py"):
                tests.append(os.path.join(root, file))
    return tests


def main(args):
    tests = get_all_tests(args.filter)
    for test in tests:
        # running using action load module
        results = subprocess.check_output(f"python {test}", shell=True)
        results = list(map(int, results.splitlines()[-1].decode("utf-8").split()))
        if not all(results[:2]):
            return Exception(f"Test {test} failed")

        # running using action load local
        results = subprocess.check_output(f"python {test} --local", shell=True)
        results = list(map(int, results.splitlines()[-1].decode("utf-8").split()))
        if not all(results[:2]):
            return Exception(f"Test {test} failed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tests for jaseci_ai_kit")
    parser.add_argument("--filter", type=str, help="Filter tests")
    args = parser.parse_args()

    main(args)
