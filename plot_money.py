import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
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
APP = [
    "sentence_pairing",
    "discussion_analysis",
    "flight_chatbot",
    "restaurant_chatbot",
    "zeroshot_faq_bot",
    "flow_analysis",
]
METRIC = ["average_latency", "throughput", "99th_latency"]
MEMS = [4, 6, 8]

DIRECTORY = "synthetic_apps_results"
# FILE = f"synthetic_apps_results.json"
# with open(FILE, "r") as fin:
#     results = json.load(fin)

for app in APP:
    for metric in METRIC:
        # get all local and all remote result
        mem_4_result_file = os.path.join(DIRECTORY, f"{app}-4.json")
        # A hack some data is missing atm
        if not os.path.isfile(mem_4_result_file):
            mem_4_result_file = os.path.join(DIRECTORY, f"{app}-6.json")
        with open(mem_4_result_file, "r") as fin:
            data = json.load(fin)[app]
        all_local = data["all_local"]["walker_level"]["walker_run"]["all"][metric]
        all_remote = data["all_remote"]["walker_level"]["walker_run"]["all"][metric]

        # turn this into a list of one so we can have different bar colors
        all_local = [all_local]
        all_remote = [all_remote]

        eval_lats = []
        eval_legends = []
        for mem in MEMS:
            mem_result_file = os.path.join(DIRECTORY, f"{app}-{mem}.json")
            if not os.path.isfile(mem_result_file):
                continue
            with open(mem_result_file, "r") as fin:
                data = json.load(fin)[app]
            policy_key = f"evaluation-mem-{mem*1024}"
            eval_legends.append(f"Eval-{mem}GiB")
            eval_res = data[policy_key]["walker_level"]["walker_run"]["all"][metric]
            # normalize to all remote
            if "latency" in metric:
                eval_res = list(np.divide(all_remote, eval_res))
            elif "throughput" in metric:
                eval_res = list(np.divide(eval_res, all_remote))
            eval_lats.append(eval_res)

        if "latency" in metric:
            all_local = list(np.divide(all_remote, all_local))
        elif "throughput" in metric:
            all_local = list(np.divide(all_local, all_remote))
        all_remote = list(np.divide(all_remote, all_remote))
        # avg_lats = []
        # for policy in POLICIES:
        #     avg_lats.append(
        #         [results[app][policy]["walker_level"]["walker_run"]["all"][metric]]
        #     )
        br_all_remote = np.arange(len(all_remote))  # 1 for all remote
        brs_eval = []
        for i in range(len(eval_lats)):
            brs_eval.append([x + barWidth * (i + 1) for x in br_all_remote])
        br_all_local = [x + barWidth for x in brs_eval[-1]]

        # Set position of bar on X axis
        # br1 = np.arange(1)
        # br2 = [x + barWidth for x in br1]
        # br3 = [x + barWidth for x in br2]
        # br4 = [x + barWidth for x in br3]
        # br5 = [x + barWidth for x in br4]

        # if "latency" in metric:
        #     all_local = list(np.divide(avg_lats[0], avg_lats[1]))
        #     regular_reeval = list(np.divide(avg_lats[0], avg_lats[2]))
        #     all_remote = list(np.divide(avg_lats[0], avg_lats[0]))
        # elif "throughput" in metric:
        #     all_local = list(np.divide(avg_lats[1], avg_lats[0]))
        #     regular_reeval = list(np.divide(avg_lats[2], avg_lats[0]))
        #     all_remote = list(np.divide(avg_lats[0], avg_lats[0]))

        def y_fmt(x, y):
            return f"{int(y)}X"

        fig, ax = plt.subplots(figsize=(6, 6))
        formatter = tick.FormatStrFormatter("?%1.1f")
        # ax.yaxis.set_major_formatter(formatter)
        ax.axhline(y=1, ls="--", color="black")
        # ax.set_yticks([1.0, 2.0, 3.0, 4.0])
        ax.set_ylim(0.8, 1.2)

        # Make the plot
        ax.bar(
            br_all_remote,
            all_remote,
            color="dimgray",
            width=barWidth,
            hatch="x",
            edgecolor="grey",
            label="All Remote",
        )
        # ax.bar(br2, all_local_avg_lat, color ='silver', width = barWidth,
        #     edgecolor ='grey', label ='All Local')
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
        ax.bar(
            br_all_local,
            all_local,
            color="darkturquoise",
            width=barWidth,
            hatch="+",
            edgecolor="grey",
            label="All local",
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
        plt.legend(fontsize=12)

        plt.savefig(f"{DIRECTORY}/{app}-{metric}.pdf", bbox_inches="tight")
