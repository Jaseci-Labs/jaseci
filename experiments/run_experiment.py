import requests
import config
from util import authenticate  # , port_fowrward
import os
import json
import time
import argparse

# import asyncio
import traceback

# Port forward
# port_fowrward()

# Authenticate
token = authenticate()

all_experiments = [
    "sentence_pairing",
    "discussion_analysis",
    "restaurant_chatbot",
    "flight_chatbot",
    "zeroshot_faq_bot",
    "flow_analysis",
    "virtual_assistant",
]
no_local_config = [
    "flight_chatbot",
    "zeroshot_faq_bot",
    "flow_analysis",
    "virtual_assistant",
]

all_policy_config = ["all_local", "evaluation", "all_remote"]


def run_experiments(
    experiment_folder_name,
    app_name,
    run_number,
    experiment_duration=300,
    eval_phase=10,
    perf_phase=100,
    policy_configs=None,
):
    mem = 4

    if policy_configs is None:
        if app_name in no_local_config:
            policy_configs = all_policy_config[1:]
        else:
            policy_configs = all_policy_config
    headers = {"content-type": "application/json", "Authorization": f"Token {token}"}
    for policy in policy_configs:
        try:
            payload = {
                "test": "synthetic_apps",
                "experiment": app_name,
                "mem": mem,
                "policy": policy,
                "experiment_duration": experiment_duration,
                "eval_phase": eval_phase,
                "pref_phase": perf_phase,
            }
            result = requests.post(
                url=config.url + "/js_admin/jsorc_loadtest",
                headers=headers,
                json=payload,
                timeout=None,
            )
        except Exception as e:
            print(e)
            traceback.print_exc()

        time.sleep(20)
        print(result.json())
        f_name = os.path.join(
            f"{experiment_folder_name}/{app_name}/run_{run_number}",
            f"{app_name}-{4}.json",
        )
        if os.path.exists(f_name):
            print(f"file: {f_name} exists, updating")
            with open(f_name, "r+") as fp:
                file_data = json.load(fp)
                if policy == "evaluation":
                    policy = "evaluation-mem-4096"
                file_data[app_name][policy] = result.json()[app_name][policy]
                fp.seek(0)
                json.dump(file_data, fp, indent=4)
        else:
            os.makedirs(
                f"{experiment_folder_name}/{app_name}/run_{run_number}",
                exist_ok=True,
            )
            with open(f_name, "w") as fp:
                json.dump(result.json(), fp, indent=4)
            print(f"File '{f_name}' created and updated successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-ef",
        "--experiment-folder",
        default="experiments",
        help="Experiment folder name",
    )
    parser.add_argument(
        "-a", "--app-name", required=True, help="Name of the application"
    )
    parser.add_argument(
        "-r", "--run-number", type=int, default=1, help="Run number of the experiment"
    )
    parser.add_argument(
        "-ed",
        "--experiment-duration",
        type=int,
        default=300,
        help="Duration of the experiment in seconds",
    )
    parser.add_argument(
        "-ep",
        "--eval-phase",
        type=int,
        default=10,
        help="Evaluation phase duration in seconds",
    )
    parser.add_argument(
        "-pp",
        "--perf-phase",
        type=int,
        default=100,
        help="Performance phase duration in seconds",
    )
    parser.add_argument(
        "-pc", "--policy-config", default=None, help="Policy configuration"
    )
    args = parser.parse_args()

    experiment_folder_name = args.experiment_folder
    app_name = args.app_name
    run_number = args.run_number
    experiment_duration = args.experiment_duration
    eval_phase = args.eval_phase
    perf_phase = args.perf_phase
    if args.policy_config is not None:
        policy_config = [args.policy_config]
    else:
        policy_config = args.policy_config
    run_experiments(
        experiment_folder_name,
        app_name,
        run_number,
        experiment_duration,
        eval_phase,
        perf_phase,
        policy_config,
    )
