import subprocess
import argparse
import os
import traceback


def get_all_tests(filter_str: str):
    tests = []
    for root, _, files in os.walk(os.getcwd()):
        for file in files:
            if file.startswith(str(filter_str)) and file.endswith(".py"):
                tests.append(os.path.join(root, file))
    return tests


def main(args):
    tests = get_all_tests(args.filter)

    if len(tests) == 0:
        print("No tests found")
        return

    for test in tests:
        try:
            # running using action load module
            print(
                f"\n {'+' * 10} Running test {test} using action load module {'+' * 10} \n"
            )
            results = subprocess.check_output(f"python {test}", shell=True)
            results = list(map(int, results.splitlines()[-1].decode("utf-8").split()))
            if any(results[:2]):
                return Exception("Test failed")

            # running using action load local
            print(
                f"\n {'+' * 10} Running test {test} using action load local {'+' * 10} \n"
            )
            results = subprocess.check_output(f"python {test} --local", shell=True)
            results = list(map(int, results.splitlines()[-1].decode("utf-8").split()))
            if any(results[:2]):
                return Exception("Test failed")

            # running using action load remote
            print(
                f"\n {'+' * 10} Running test {test} using action load remote {'+' * 10} \n"
            )
            # getting the minikube ip
            ip = (
                subprocess.check_output("minikube ip", shell=True)
                .decode("utf-8")
                .strip()
            )
            # #deploy the pod
            # subprocess.check_output(f"kubectl apply -f {None}", shell=True)
            port = "30589"  # TODO: get the port from the yaml file
            results = subprocess.check_output(
                f"python {test} --remote http://{ip}:{port}", shell=True
            )
            results = list(map(int, results.splitlines()[-1].decode("utf-8").split()))
            if any(results[:2]):
                return Exception("Test failed")

        except Exception as e:
            traceback.print_exc()
            return e


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tests for jaseci_ai_kit")
    parser.add_argument("--filter", type=str, help="Filter tests")
    args = parser.parse_args()

    main(args)
