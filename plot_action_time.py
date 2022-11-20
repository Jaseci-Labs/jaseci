import re
import numpy as np
import pandas as pd
import os
from collections import OrderedDict
import json

import matplotlib.pyplot as plt

from datetime import datetime

# link_mode = "remotely_linked"
# Convert the duration column to milliseconds
def convert_to_ms(value):
    return int(
        (datetime.strptime(value, "%H:%M:%S.%f") - datetime(1900, 1, 1)).total_seconds()
        * 1000
    )


def clean_data(df):
    # df['Duration'] = df['Duration'].apply(convert_to_ms)
    return df.drop(columns=["Start Time", "End Time"])


label_dict = OrderedDict(
    {
        "bi_enc.cosine_sim": "bi/cos",
        "bi_enc.dot_prod": "bi/dot",
        "bi_enc.get_candidate_emb": "bi/emb1",
        "bi_enc.get_context_emb": "bi/emb2",
        "bi_enc.infer": "bi/infer",
        "cl_summer.summarize": "sum/sum",
        "ent_ext.entity_detection": "fner/infer",
        "flair_ner.entity_detection": "fner/infer",
        "tfm_ner.extract_entity": "tner/infer",
        "use_enc.cos_sim_score": "use/cos",
        "use_enc.encode": "use/enc",
        "use_enc.text_classify": "use/clf",
        "use_enc.text_similarity": "use/sim",
        "use_qa.answer_classify": "qa/aclf",
        "use_qa.answer_encode": "qa/aenc",
        "use_qa.answer_similarity": "qa/asim",
        "use_qa.cos_sim_score": "qa/cos",
        "use_qa.dist_score": "qa/dist",
        "use_qa.qa_classify": "qa/clf",
        "use_qa.qa_similarity": "qa/sim",
        "use_qa.question_classify": "qa/qclf",
        "use_qa.question_encode": "qa/qenc",
        "use_qa.question_similarity": "qa/qsim",
        "text_seg.get_segments": "seg/text",
    }
)


def plot_bar(plt):
    # df = df.reset_index()
    # # ax.set_title(df.at[0, 'Module Name'])
    # df["full_name"] = df["Module Name"] + "/" + df["Action Name"]
    # print(df)
    # df_local = df[df["Local/Remote"] == "local"]
    # df_local = df_local.pivot(
    #     index="full_name", values="Duration", columns="Local/Remote"
    # )

    # df_remote = df[df["Local/Remote"] == link_mode]
    # df_remote = df_remote.pivot(
    #     index="full_name", values="Duration", columns="Local/Remote"
    # )

    # df_final = pd.concat([df_local, df_remote], axis=1)
    # df_final["Relative increase"] = (df_final[link_mode]) / df_final["local"]
    # df_final = df_final.drop(columns=["local", link_mode])
    # print(df_final)
    # print(df_final.columns.tolist())
    # print(df_final.index)

    # for k,v in label_dict.items():
    #     df_final.loc[df_final["Index"] == k, "Index"] = v
    # print(df_final)
    # ax.xaxis.label.set_visible(False)
    # ax.axhline(y=1, ls="--", color = "black")
    # ax.tick_params(top=False, bottom=False, left=False, right=False)

    data = {}
    for res_file in os.listdir("action_level_results"):
        with open(os.path.join("action_level_results", res_file), "r") as fin:
            d = json.load(fin)
            data.update(d)

    # with open("action_level_test_11_16.json", "r") as fin:
    #     data = json.load(fin)
    x_labels = []
    y_values = []
    for action_set, as_result in data.items():
        for action, action_result in as_result.items():
            x_label = f"{action_set}.{action}"
            y_value = action_result["remote_over_local"]["average_latency"]
            x_labels.append(label_dict[x_label])
            y_values.append(y_value)

    print(x_labels)
    print(y_values)

    fig, ax = plt.subplots()
    plt.ylabel("Normalized AVG Latency")
    ax.yaxis.set_major_formatter("{x}X")
    ax.axhline(y=1, ls="--", color="black")
    ax.bar(range(len(y_values)), y_values, align="center")
    # ax.bar(df_final.index, df_final["Relative increase"])
    plt.xticks(rotation=90, ha="center")
    xticks = range(len(y_values))
    xticks = [x for x in xticks]
    ax.set_xticks(xticks)
    ax.set_xticklabels(x_labels)
    # df_final.plot.bar(legend = None)


def get_unique_values(df, column):
    return df[column].unique()


def main() -> None:
    # df = pd.read_csv(in_file)

    # # remove useless columns and convert the duration column to actual seconds
    # df = clean_data(df)

    # # drop these values, because ... feelings!!
    # print("===========")
    # print(df)
    # df.drop(df[df["Module Name"] == "text_seg"].index, inplace=True)
    # df.drop(df[df["Module Name"] == "pdf_ext"].index, inplace=True)
    # df.drop(df[df["Module Name"] == "flair_ner"].index, inplace=True)
    # print(df)
    # modules = get_unique_values(df, "Module Name")

    # # count the occurance of each module to generate the relative widths of each graph
    # ratio = list(df["Module Name"].value_counts(sort=False))

    plot_bar(plt)
    # fig, axs = plt.subplots(1, len(modules),figsize=(10, 4), sharey=True, gridspec_kw={'width_ratios': ratio})
    # for module, ax in zip(modules, axs):
    #     plot_bar(df[df['Module Name'] == module], ax)

    # make the legend of the last graph, the overall legend
    # handles, labels = axs[-1].get_legend_handles_labels()
    # fig.legend(handles, labels, loc='lower center', ncol = 2, bbox_to_anchor=(0.5, 1))

    # fig.supylabel('Normalized Latency', x = 0, y = 0.65)

    # fig.tight_layout(pad=0.0)
    fig = plt.gcf()
    fig.set_size_inches(6, 3)
    plt.savefig("action_level_avg_latency.pdf", bbox_inches="tight")


if __name__ == "__main__":
    # folder = "../../jaseci_data/action_level_test/8_12_action_level_test/"
    # path = '../../jaseci_data/action_level_test/8_12_action_level_test/time.csv'
    main()
    # folder = "./"
    # path = os.path.join(folder, "time.csv")
    # for link_mode in ["locally_linked", "remotely_linked"]:
    #     # out_path = f"../../jaseci_data/action_level_test/8_12_action_level_test/rel_time_{link_mode}.pdf"
    #     # out_path = os.path.join(folder, f"rel_time_{link_mode}.pdf")
    #     out_path = os.path.join(folder, "microbenchmark.pdf")
    #     main(path, out_file=out_path, link_mode=link_mode)
