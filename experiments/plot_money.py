import numpy as np
import matplotlib.pyplot as plt

# import matplotlib.ticker as tick
import os
import json
import sys

# import glob

# Set the width of each bar
barWidth = 0.1

# Constants
TECH = [
    "default",
    "regular_reevaluation",
    "action_pressure_trigger",
    "action_pressure_trigger_prediction",
    "oracle",
]
POLICIES = ["all_remote", "all_local", "evaluation"]

ALL_CONFIG_APP = [
    "sentence_pairing",
    "discussion_analysis",
    "restaurant_chatbot",
]

# Check if directory path is provided
if len(sys.argv) < 2:
    print("Please provide the directory path as a command-line argument.")
    sys.exit(1)

# Get the folder name from the command-line argument
folder_name = sys.argv[1]

# # Get the list of JSON files in the folder
# files = glob.glob(f"{folder_name}/*.json")
# module_name = [os.path.basename(f_name).split("-")[0] for f_name in files]

app_run_results = {}

# Recursively find all JSON files in the folder and subfolders
for root, dirs, files in os.walk(folder_name):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            with open(file_path, "r") as fin:
                run_data = json.load(fin)
                module_name = os.path.basename(file_path).split("-")[0]
                if module_name not in app_run_results:
                    app_run_results[module_name] = []
                app_run_results[module_name].append(run_data)

METRIC = ["average_latency", "throughput", "99th_latency"]
# MEMS = [4, 6, 8]
MEMS = [4]
# Process each application
for app, run_results in app_run_results.items():
    print(f"Started processing for {app}")
    local_app = app in ALL_CONFIG_APP
    for metric in METRIC:
        all_remote_list = []
        eval_lats_list = []
        all_local_list = []
        for run_data in run_results:
            # mem_4_result_file = os.path.join(folder_name, f"{app}-4.json")
            # if not os.path.isfile(mem_4_result_file):
            #     mem_4_result_file = os.path.join(folder_name, f"{app}-6.json")
            # with open(mem_4_result_file, "r") as fin:
            #     data = json.load(fin).get(app, {})

            # Extract data for all_remote
            data = run_data.get(app, {})
            all_remote = (
                data.get("all_remote", {})
                .get("walker_level", {})
                .get("walker_run", {})
                .get("all", {})
                .get(metric, [])
            )
            all_remote = [all_remote]
            all_remote_list.append(all_remote)
            # Extract data for evaluation
            eval_lats = []
            eval_legends = []
            for mem in MEMS:
                # mem_result_file = os.path.join(folder_name, f"{app}-{mem}.json")
                # if not os.path.isfile(mem_result_file):
                #     continue
                # with open(mem_result_file, "r") as fin:
                #     data = json.load(fin).get(app, {})

                policy_key = f"evaluation-mem-{mem*1024}"
                eval_legends.append(f"Eval-{mem}GiB")
                eval_res = (
                    data.get(policy_key, {})
                    .get("walker_level", {})
                    .get("walker_run", {})
                    .get("all", {})
                    .get(metric, [])
                )
                if "latency" in metric:
                    eval_res = list(np.divide(all_remote, eval_res))
                elif "throughput" in metric:
                    eval_res = list(np.divide(eval_res, all_remote))
                eval_lats.append(eval_res)
            eval_lats_list.append(eval_lats)
            # Calculate local speedup for local apps
            if local_app:
                all_local = (
                    data.get("all_local", {})
                    .get("walker_level", {})
                    .get("walker_run", {})
                    .get("all", {})
                    .get(metric, [])
                )
                all_local = [all_local]
                if "latency" in metric:
                    all_local = list(np.divide(all_remote, all_local))
                elif "throughput" in metric:
                    all_local = list(np.divide(all_local, all_remote))
                all_local_list.append(all_local)
        all_remote = np.mean(all_remote_list, axis=0)
        eval_lats = np.mean(eval_lats_list, axis=0)
        if local_app:
            all_local = np.mean(all_local_list, axis=0)
        # Normalize all_remote values to 1
        all_remote = list(np.divide(all_remote, all_remote))

        # Prepare bar positions for evaluation
        br_all_remote = np.arange(len(all_remote))
        brs_eval = [br_all_remote + barWidth * (i + 1) for i in range(len(eval_lats))]

        # Prepare bar positions for local apps
        if local_app:
            br_all_local = (
                [br_all_remote + barWidth * (len(eval_lats) + 1)] if eval_lats else []
            )

        # Create the plot
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.axhline(y=1, ls="--", color="black")
        ax.bar(
            br_all_remote,
            all_remote,
            color="dimgray",
            width=barWidth,
            hatch="x",
            edgecolor="grey",
            label="All Remote",
        )

        for i in range(len(brs_eval)):
            ax.bar(
                brs_eval[i],
                eval_lats[i],
                color="paleturquoise",
                width=barWidth,
                hatch="||",
                edgecolor="grey",
                label=eval_legends[i],
            )

        # Plot bars for local apps
        if local_app and br_all_local:
            ax.bar(
                br_all_local[0],
                all_local,
                color="darkturquoise",
                width=barWidth,
                hatch="+",
                edgecolor="grey",
                label="All Local",
            )

        plt.ylabel(f"{metric} Speedup (X)", fontsize=16)
        plt.xticks([])
        plt.legend(fontsize=12)

        # Save the plot as PDF
        plt.savefig(f"{folder_name}/{app}/{app}-{metric}.pdf", bbox_inches="tight")
        plt.close(fig)

print("Processing completed.")
