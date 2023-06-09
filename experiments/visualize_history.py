import json
import matplotlib.pyplot as plt
import sys
import math
import glob
import os


def roundup(x):
    return int(math.ceil(x / 100.0)) * 100


def visualize_config_change(config_history, final_clock, fig_fname):
    # Group the configuration based on local vs remote
    # and plot scatter plots with different colors
    module_list = list(config_history[1]["actions_state"].keys())
    y_values = {val: i + 1 for i, val in enumerate(module_list)}
    local_dots = {"x": [], "y": []}
    remote_dots = {"x": [], "y": []}

    local_color = "tab:red"
    local_marker = "o"

    remote_color = "tab:blue"
    remote_marker = "x"

    start_ts = config_history[0]["ts"]
    end_ts = config_history[-1]["ts"]

    for entry in config_history:
        ts = int(entry["ts"] - start_ts)
        if "actions_state" not in entry:
            continue
        for comp, layout in entry["actions_state"].items():
            if comp not in y_values:
                continue
            if layout["mode"] == "module":  # local
                local_dots["x"].append(ts)
                local_dots["y"].append(y_values[comp])
            elif layout["mode"] == "remote":  # remote
                remote_dots["x"].append(ts)
                remote_dots["y"].append(y_values[comp])
            else:
                raise Exception(f"Invalid layout value {entry}")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(
        local_dots["x"],
        local_dots["y"],
        color=local_color,
        marker=local_marker,
        s=30,
        label="Local",
    )
    ax.scatter(
        remote_dots["x"],
        remote_dots["y"],
        color=remote_color,
        marker=remote_marker,
        s=30,
        label="Remote",
    )

    ax.set_ylim(0, len(module_list) + 1)
    ax.set_yticks(list(y_values.values()))
    ax.set_yticklabels(module_list)
    ax.set_xticks(local_dots["x"])
    ax.set_xticklabels(local_dots["x"], rotation=90)
    ax.set_xlim(0, roundup(end_ts - start_ts))
    ax.set_xlabel("Time")
    ax.set_ylabel("Module")
    ax.set_title("Configuration Change History")
    ax.legend(loc="upper left")

    plt.tight_layout()
    plt.savefig(fig_fname)
    plt.show()


if len(sys.argv) < 2:
    print("Please provide the directory path as a command-line argument.")
    sys.exit(1)

folder_name = sys.argv[1]


files = glob.glob(f"{folder_name}/*.json")
module_name = [os.path.basename(f_name).split("-")[0] for f_name in files]

if __name__ == "__main__":
    for module in module_name:
        print(f"Started processing for {module}")
        result_json = f"{folder_name}/{module}-4.json"
        with open(result_json, "r") as fin:
            result = json.load(fin)
            config_history = result[module]["evaluation-mem-4096"]["action_level"]
            # final_clock = result["final_clock"]
        visualize_config_change(
            config_history, 0, f"{folder_name}/{module}_act_hist.pdf"
        )
    print("Processing completed.")
