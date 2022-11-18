import numpy as np
import matplotlib.pyplot as plt
import os
import json
import csv
import copy

# set width of bar
barWidth = 0.1

# set height of bar
TRACES = ["dynamic"]
MEM = "8g"
RESULT_DIR = f"dynamic_regular_eval_no_queue_mem_{MEM}"

TECH = [
    "default",
    "regular_reevaluation",
    "action_pressure_trigger",
    "action_pressure_trigger_prediction",
    "oracle",
]
POLICIES = ["all_remote", "all_local", "evaluation"]
APP = ["sentence_pairing", "discussion_analysis"]
METRIC = ["average_latency", "throughput", "99th_latency"]

FILE = f"synthetic_apps_results.json"
with open(FILE, "r") as fin:
    results = json.load(fin)


for app in APP:
    for metric in METRIC:
        avg_lats = []
        for policy in POLICIES:
            avg_lats.append(
                [results[app][policy]["walker_level"]["walker_run"]["all"][metric]]
            )

        # Set position of bar on X axis
        br1 = np.arange(1)
        br2 = [x + barWidth for x in br1]
        br3 = [x + barWidth for x in br2]
        br4 = [x + barWidth for x in br3]
        br5 = [x + barWidth for x in br4]

        if "latency" in metric:
            all_local = list(np.divide(avg_lats[0], avg_lats[1]))
            regular_reeval = list(np.divide(avg_lats[0], avg_lats[2]))
            all_remote = list(np.divide(avg_lats[0], avg_lats[0]))
        elif "throughput" in metric:
            all_local = list(np.divide(avg_lats[1], avg_lats[0]))
            regular_reeval = list(np.divide(avg_lats[2], avg_lats[0]))
            all_remote = list(np.divide(avg_lats[0], avg_lats[0]))

        fig, ax = plt.subplots(figsize=(4, 6))
        ax.yaxis.set_major_formatter("{x}X")
        ax.axhline(y=1, ls="--", color="black")
        # ax.set_yticks([1.0, 2.0, 3.0, 4.0])
        # ax.set_ylim(0.9, 4.0)

        # Make the plot
        ax.bar(
            br1,
            all_remote,
            color="dimgray",
            width=barWidth,
            hatch="x",
            edgecolor="grey",
            label="All Remote",
        )
        # ax.bar(br2, all_local_avg_lat, color ='silver', width = barWidth,
        #     edgecolor ='grey', label ='All Local')
        ax.bar(
            br2,
            all_local,
            color="darkturquoise",
            width=barWidth,
            hatch="+",
            edgecolor="grey",
            label="All local",
        )
        ax.bar(
            br3,
            regular_reeval,
            color="paleturquoise",
            width=barWidth,
            hatch="||",
            edgecolor="grey",
            label="Fixed-Int.",
        )
        # ax.bar(
        #     br4,
        #     action_pressure_trigger_prediction,
        #     color="cadetblue",
        #     width=barWidth,
        #     hatch="//",
        #     edgecolor="grey",
        #     label="AP Pred.",
        # )
        # ax.bar(
        #     br5,
        #     oracle,
        #     color="silver",
        #     width=barWidth,
        #     hatch=".",
        #     edgecolor="grey",
        #     label="Oracle",
        # )

        # Adding Xticks
        # plt.xlabel('Trace', fontweight ='bold', fontsize = 10)
        plt.ylabel(f"{metric} Speedup (X)", fontsize=16)
        # plt.xticks([r + barWidth for r in range(len(avg_lats[0]))], TRACES)
        plt.xticks([])
        # plt.title("Dynamic Trace, Different JSORC Tech, with node memory capacity=2GB")

        # plt.legend(fontsize=14, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.24))
        plt.legend(fontsize=16)

        plt.savefig(f"{app}-{metric}.pdf", bbox_inches="tight")
