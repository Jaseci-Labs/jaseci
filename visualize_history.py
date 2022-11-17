import json
from re import I
from threading import local
import matplotlib.pyplot as plt


def visualize_config_change(config_history, final_clock, fig_fname):
    # Group the configuration based local vs remote and plot scatter plots with different colors
    y_values = {
        # "bi_enc": 1,
        # "tfm_ner": 2,
        # "use_enc": 2,
        # "use_qa": 4,
        # "cl_summer": 5,
        "text_seg": 1,
        "use_qa": 2,
    }
    local_dots = {"x": [], "y": []}
    remote_dots = {"x": [], "y": []}

    local_color = "r"
    local_marker = "o"

    remote_color = "b"
    remote_marker = "x"

    start_ts = config_history[0]["ts"]
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

    print(local_dots["x"])
    print(local_dots["y"])
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.scatter(
        local_dots["x"],
        local_dots["y"],
        color=local_color,
        marker=local_marker,
        size=20,
        label="local",
    )
    ax.scatter(
        remote_dots["x"],
        remote_dots["y"],
        color=remote_color,
        marker=remote_marker,
        size=20,
        label="remote",
    )

    ax.set_ylim(0, 6)
    # ax.set_yticks([1, 2, 3, 4, 5])
    # ax.set_yticklabels(["bi_enc", "tfm_ner", "use_enc", "use_qa", "cl_summer"])

    ax.set_yticks([1, 2])
    ax.set_yticklabels(["bi_enc", "use_enc"])
    ax.set_xticks(local_dots["x"])
    ax.set_xticklabels(local_dots["x"], rotation=90)
    ax.set_xlim(0, 100)
    ax.legend()
    plt.savefig(fig_fname)


if __name__ == "__main__":
    result_json = "zeroshot_faq_results.json"
    with open(result_json, "r") as fin:
        result = json.load(fin)
        config_history = result["zeroshot_faq_bot"]["evaluation"]["action_level"]
        # final_clock = result["final_clock"]

    visualize_config_change(config_history, 0, "zeroshot_faq_history.pdf")
