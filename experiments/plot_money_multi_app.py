import numpy as np
import matplotlib.pyplot as plt
import json
import sys
import os

# Set the width of each bar
barWidth = 0.2

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
    # "sentence_pairing",
    # "discussion_analysis",
    # "restaurant_chatbot",
]

# Check if file name is provided
if len(sys.argv) < 2:
    print("Please provide the file name as a command-line argument.")
    sys.exit(1)

# Get the file name from the command-line argument
file_name = sys.argv[1]

# Load the JSON data from the file
with open(file_name, "r") as fp:
    app_run_results = json.load(fp)

METRIC = ["average_latency", "throughput", "99th_latency"]
MEM = 4

# Process each application
for app, data in app_run_results.items():
    print(f"Started processing for {app}")
    local_app = app in ALL_CONFIG_APP
    for metric in METRIC:
        all_remote_list = []
        eval_lats_list = []
        all_local_list = []

        all_app = list(
            data.get("all_remote", {})
            .get("walker_level", {})
            .get("walker_run", {})
            .keys()
        )[:-1]

        for app_key in all_app:
            all_remote = (
                data.get("all_remote", {})
                .get("walker_level", {})
                .get("walker_run", {})
                .get(app_key, {})
                .get(metric, [])
            )

            # Extract data for evaluation
            eval_lats = []
            eval_legends = []
            policy_key = f"evaluation-mem-{MEM*1024}"
            eval_legends.append(f"Eval-{MEM}-GiB")
            eval_res = (
                data.get(policy_key, {})
                .get("walker_level", {})
                .get("walker_run", {})
                .get(app_key, {})
                .get(metric, [])
            )
            # print(eval_res)
            if "latency" in metric:
                eval_res = all_remote / eval_res
            elif "throughput" in metric:
                eval_res = eval_res / all_remote

            # eval_lats.append(eval_res)
            eval_lats_list.append(eval_res)

            # Calculate local speedup for local apps
            if local_app:
                all_local = (
                    data.get("all_local", {})
                    .get("walker_level", {})
                    .get("walker_run", {})
                    .get("all", {})
                    .get(metric, [])
                )

                if "latency" in metric:
                    all_local = np.divide(all_remote, all_local)
                elif "throughput" in metric:
                    all_local = np.divide(all_local, all_remote)

                all_local_list.append(all_local)
        # Normalize all_remote values to 1
        all_remote_list = [1] * len(all_app)

        # Prepare bar positions for evaluation
        br_all_remote = np.arange(len(all_app))
        brs_eval = [barWidth + i for i in range(len(br_all_remote))]

        # Prepare bar positions for local apps
        if local_app:
            br_all_local = [2 * barWidth + i for i in range(len(br_all_remote))]

        # print(all_remote_list, all_local_list, eval_lats_list)
        # Create the plot
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.axhline(y=1, ls="--", color="black")
        ax.bar(
            br_all_remote,
            all_remote_list,
            color="dimgray",
            width=barWidth,
            hatch="x",
            edgecolor="grey",
            linewidth=1.0,
            label="All Remote",
        )

        ax.bar(
            brs_eval,
            eval_lats_list,
            color="paleturquoise",
            width=barWidth,
            hatch="||",
            edgecolor="grey",
            linewidth=1.0,
            label=eval_legends[0],
        )

        # Plot bars for local apps
        if local_app and br_all_local:
            ax.bar(
                br_all_local,
                all_local_list,
                color="darkturquoise",
                width=barWidth,
                hatch="+",
                edgecolor="grey",
                linewidth=1.0,
                label="All Local",
            )

        plt.ylabel(f"{metric} Speedup (X)", fontsize=16)
        plt.xticks([r + barWidth for r in range(len(all_app))], all_app)
        plt.legend(fontsize=12)
        plt.tight_layout()
        # Save the plot as PDF in the parent directory of the input file
        parent_directory = os.path.dirname(file_name)
        output_file = os.path.join(parent_directory, f"{app}-{metric}.pdf")
        plt.savefig(output_file, bbox_inches="tight")
        plt.close(fig)

print("Processing completed.")
