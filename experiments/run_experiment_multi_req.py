import requests
import config
from util import authenticate  # , port_fowrward
import os
import json
import time
import argparse

# import asyncio
import traceback
import threading

# Port forward
# port_fowrward()
app_freq_pairs = [
    ("zeroshot_faq_bot", 1),
    ("flow_analysis", 2),
    # ("discussion_analysis", 2),
    # ("disc_analysis", 2),
    # ("restaurant_chatbot", 3),
    # ("sentence_pairing", 4),
    # ("virtual_assistant", 1),
]
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
    "disc_analysis",
]
no_local_config = [
    "flight_chatbot",
    "zeroshot_faq_bot",
    "flow_analysis",
    "virtual_assistant",
]

# all_policy_config = ["all_local", "auto", "all_remote"]
# all_policy_config = ["auto", "all_remote"]
all_policy_config = ["all_remote"]
APP_PATH = "/home/ubuntu/jaseci/jaseci_serv/jaseci_serv/base/example_jac"


app_to_actions = {
    "zeroshot_faq_bot": ["jac_nlp.text_seg", "jac_nlp.use_qa"],
    "sentence_pairing": ["jac_nlp.sbert_sim", "jac_nlp.bi_enc"],
    "discussion_analysis": ["jac_nlp.bi_enc", "jac_nlp.cl_summer"],
    "disc_analysis": ["jac_nlp.sbert_sim", "jac_nlp.cl_summer"],
    "flight_chatbot": ["jac_nlp.use_qa", "jac_nlp.ent_ext"],
    "restaurant_chatbot": ["jac_nlp.bi_enc", "jac_nlp.tfm_ner"],
    "virtual_assistant": [
        # "jac_nlp.text_seg",
        "jac_nlp.bi_enc",
        "jac_nlp.tfm_ner",
        "jac_nlp.sbert_sim",
        "jac_nlp.use_qa",
    ],
    "flow_analysis": [
        "jac_nlp.sbert_sim",
        "jac_nlp.tfm_ner",
        "jac_nlp.use_qa",
    ],
    "weather_and_time_assitance": [
        "jac_speech.vc_tts",
        "jac_speech.stt",
        "jac_nlp.bi_enc",
    ],
}
st_time = time.time()


def make_walker_run_request(snt_id, headers, app_name, freq, experiment_duration):

    # Define the payload for the walker run request
    payload = {"name": app_name, "ctx": {}, "snt": snt_id}
    # interval = 1 / freq
    start_time = time.time()
    while (time.time() - start_time) < experiment_duration:
        requests.post(url=config.url + "/js/walker_run", headers=headers, json=payload)
        # time.sleep(interval)  # Adjust the duration as needed


loaded_apps = []


def sent_reg(app_name, headers, mode):
    jac_file = os.path.join(APP_PATH, f"{app_name}.jac")
    jac_code = open(jac_file).read()
    payload = {"code": jac_code, "opt_level": 2, "name": app_name}

    sent_data = requests.post(
        url=config.url + "/js/sentinel_register", headers=headers, json=payload
    )
    # Load models that are not already loaded
    for module in app_to_actions[app_name]:
        package, act_name = module.split(".")
        payload = {"name": act_name}
        res = requests.post(
            url=config.url + "/js_admin/jsorc_actions_status",
            headers=headers,
            json=payload,
        )
        if res.status_code == 200:
            if (
                res.json()["action_status"] is None
                or res.json()["action_status"]["mode"] is None
            ):
                payload = {
                    "config": f"{package}.config",
                    "name": act_name,
                }
                res = requests.post(
                    url=config.url + "/js_admin/jsorc_actions_config",
                    headers=headers,
                    json=payload,
                )
                if res.status_code == 200:
                    payload = {
                        "name": act_name,
                        "mode": mode,
                    }
                    res = requests.post(
                        url=config.url + "/js_admin/jsorc_actions_load",
                        headers=headers,
                        json=payload,
                    )
                    while True:
                        if res.json()["action_status"]["mode"] == payload["mode"]:
                            break
                        time.sleep(10)
                        res = requests.post(
                            url=config.url + "/js_admin/jsorc_actions_load",
                            headers=headers,
                            json=payload,
                        )
            elif res.json()["action_status"]["mode"] != mode:
                payload = {
                    "config": f"{package}.config",
                    "name": act_name,
                }
                res = requests.post(
                    url=config.url + "/js_admin/jsorc_actions_config",
                    headers=headers,
                    json=payload,
                )
                if res.status_code == 200:
                    payload = {
                        "name": act_name,
                        "mode": mode,
                    }
                res = requests.post(
                    url=config.url + "/js_admin/jsorc_actions_load",
                    headers=headers,
                    json=payload,
                )
                while True:
                    if res.json()["action_status"]["mode"] == payload["mode"]:
                        break
                    time.sleep(10)
                    res = requests.post(
                        url=config.url + "/js_admin/jsorc_actions_load",
                        headers=headers,
                        json=payload,
                    )
            else:
                print(
                    f"{act_name} already loaded: {res.json()['action_status']['mode']}"
                )
        else:
            print(f"unalbe to get status for {act_name}: {res.text}")
            return None
    return sent_data.json()


event = threading.Event()


def run_experiments(
    experiment_folder_name,
    app_name,
    run_number,
    experiment_duration=300,
    eval_phase=10,
    perf_phase=100,
    policy_configs=None,
):
    global st_time
    mem = 4
    node_mem = [int(mem) * 1024]
    if policy_configs is None:
        if app_name in no_local_config:
            policy_configs = all_policy_config[1:]
        else:
            policy_configs = all_policy_config
    headers = {
        "content-type": "application/json",
        "Authorization": f"Token {token}",
    }
    action_modules = None

    def run_walker(app_name, freq, mode):
        print(f"starting {app_name} now {time.time()-st_time}")
        sent_id = sent_reg(app_name, headers, mode)
        if sent_id is not None:
            print(sent_id)
            make_walker_run_request(
                sent_id[0]["jid"], headers, app_name, freq, experiment_duration
            )
            event.set()

    for app_name, freq in app_freq_pairs:
        if action_modules is None:
            action_modules = app_to_actions[app_name]
        else:
            action_modules = action_modules + app_to_actions[app_name]

    for policy in policy_configs:
        tasks = []
        results = {}
        try:
            if policy == "all_local" or policy == "all_remote":
                policy_params = [{}]
                jsorc_policy = "Default"
            else:
                policy_params = [{"node_mem": nm} for nm in node_mem]
                jsorc_policy = policy.capitalize()
            for pparams in policy_params:
                pparams["eval_phase"] = eval_phase
                pparams["perf_phase"] = perf_phase

                payload = {
                    "policy_name": jsorc_policy,
                    "policy_params": pparams,
                }
                requests.post(
                    url=config.url + "/js_admin/jsorc_actionpolicy_set",
                    headers=headers,
                    json=payload,
                )
                requests.post(
                    url=config.url + "/js_admin/jsorc_benchmark_start", headers=headers
                )
                requests.post(
                    url=config.url + "/js_admin/jsorc_trackact_start", headers=headers
                )
                st_time = time.time()
                for i, (app_name, freq) in enumerate(app_freq_pairs):
                    if policy == "all_local":
                        if app_name not in no_local_config:
                            task = threading.Thread(
                                target=run_walker, args=(app_name, freq, "local")
                            )
                            tasks.append(task)
                            task.start()
                    else:
                        task = threading.Thread(
                            target=run_walker, args=(app_name, freq, "remote")
                        )
                        tasks.append(task)
                        task.start()
                    if i < len(app_freq_pairs) - 1:
                        event.wait(150)  # Wait for 60 seconds or until the event is set
                        event.clear()  # Reset the event for the next thread
        except Exception as e:
            print(e)
            traceback.print_exc()

        # Wait for all threads to complete
        for task in tasks:
            task.join()

        payload = {"report": True}
        result = requests.post(
            url=config.url + "/js_admin/jsorc_benchmark_stop",
            headers=headers,
            json=payload,
        )
        action_result = requests.post(
            url=config.url + "/js_admin/jsorc_trackact_stop", headers=headers
        )
        if policy == "all_local" or policy == "all_remote":
            policy_str = policy
        else:
            policy_str = f"{'evaluation'}-mem-{pparams['node_mem']}"
        results.setdefault(app_name, {})[policy_str] = {
            "walker_level": result.json(),
            "action_level": action_result.json(),
        }
        if policy == "all_local":
            for module in action_modules:
                payload = {
                    "name": module,
                    "mode": "local",
                    "retire_svc": True,
                }
                requests.post(
                    url=config.url + "/js_admin/jsorc_actions_unload", headers=headers
                )
        elif policy == "all_remote":
            for module in action_modules:
                package, module = module.split(".")
                payload = {
                    "name": module,
                    "mode": "remote",
                    "retire_svc": False,
                }
                requests.post(
                    url=config.url + "/js_admin/jsorc_actions_unload", headers=headers
                )
        else:
            for module in action_modules:
                package, module = module.split(".")
                payload = {
                    "name": module,
                    "mode": "remote",
                    "retire_svc": False,
                }
                requests.post(
                    url=config.url + "/js_admin/jsorc_actions_unload", headers=headers
                )
        time.sleep(20)
        payload = {
            "policy_name": "Default",
            "policy_params": {},
        }
        requests.post(
            url=config.url + "/js_admin/jsorc_actionpolicy_set",
            headers=headers,
            json=payload,
        )
        print(results)
        f_name = os.path.join(
            f"{experiment_folder_name}/{app_name}/run_{run_number}",
            f"{app_name}-{4}.json",
        )
        if os.path.exists(f_name):
            print(f"file: {f_name} exists, updating")
            with open(f_name, "r+") as fp:
                file_data = json.load(fp)
                if (
                    policy == "evaluation"
                    or policy == "adaptive"
                    or policy == "predictive"
                ):
                    policy = "evaluation-mem-4096"
                file_data[app_name][policy] = results[app_name][policy]
                fp.seek(0)
                json.dump(file_data, fp, indent=4)
        else:
            os.makedirs(
                f"{experiment_folder_name}/{app_name}/run_{run_number}",
                exist_ok=True,
            )
            with open(f_name, "w") as fp:
                json.dump(results, fp, indent=4)
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
