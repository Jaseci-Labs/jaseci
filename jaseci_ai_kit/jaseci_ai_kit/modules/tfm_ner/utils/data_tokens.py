import pandas as pd


def data_token(filename):
    f = open(filename, "r", encoding="utf8")
    split_labeled_text = []
    sentence = []
    sent = 0
    for line in f:
        if len(line) == 0 or line.startswith("-DOCSTART") or line[0] == "\n":
            if len(sentence) > 0:
                split_labeled_text.append(sentence)
                sentence = []
                sent += 1
            continue
        splits = line.split(" ")
        sentence.append(("Sentence:" + str(sent), splits[0], splits[-1].rstrip("\n")))
    f.close()
    if len(sentence) > 0:
        split_labeled_text.append(sentence)
        sentence = []

    data = []
    for i in range(len(split_labeled_text)):
        for s in split_labeled_text[i]:
            data.append(s)
    df = pd.DataFrame(data, columns=["Sentence #", "Word", "Tag"])
    return df


def load_data(filename):
    # reading data from file
    data = data_token(filename)

    data["sentence"] = (
        data[["Sentence #", "Word", "Tag"]]
        .groupby(["Sentence #"])["Word"]
        .transform(lambda x: " ".join(x))
    )
    # let's also create a new column called "word_labels"
    # which groups the tags by sentence
    data["word_labels"] = (
        data[["Sentence #", "Word", "Tag"]]
        .groupby(["Sentence #"])["Tag"]
        .transform(lambda x: ",".join(x))
    )

    labels_name = sorted(list(data.Tag.unique()), reverse=True)

    data = data[["sentence", "word_labels"]].drop_duplicates().reset_index(drop=True)
    return data, labels_name
