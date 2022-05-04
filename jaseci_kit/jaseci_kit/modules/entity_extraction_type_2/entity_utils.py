from difflib import SequenceMatcher
import os


def matcher(string, pattern):
    """
    Return the start and end index of any pattern present in the text.
    """
    match_list = []
    pattern = pattern.strip()
    seqMatch = SequenceMatcher(None, string, pattern, autojunk=False)
    match = seqMatch.find_longest_match(0, len(string), 0, len(pattern))
    if match.size == len(pattern):
        start = match.a
        end = match.a + match.size
        match_tup = (start, end)
        string = string.replace(pattern, "X" * len(pattern), 1)
        match_list.append(match_tup)

    return match_list, string


def mark_sentence(s, match_list):
    """
    Marks all the entities in the sentence as per the BIO scheme.
    """
    word_dict = {}
    for word in s.split():
        word_dict[word] = "O"

    for start, end, e_type in match_list:
        temp_str = s[start:end]
        tmp_list = temp_str.split()
        if len(tmp_list) > 1:
            word_dict[tmp_list[0]] = "B-" + e_type
            for w in tmp_list[1:]:
                word_dict[w] = "I-" + e_type
        else:
            word_dict[temp_str] = "B-" + e_type
    return word_dict


def clean(text):
    """
    Just a helper fuction to add a space before
    the punctuations for better tokenization
    """
    filters = [
        "!",
        "#",
        "$",
        "%",
        "&",
        "(",
        ")",
        "/",
        "*",
        ".",
        ":",
        ";",
        "<",
        "=",
        ">",
        "?",
        "@",
        "[",
        "\\",
        "]",
        "_",
        "`",
        "{",
        "}",
        "~",
        "'",
        ",",
    ]
    for i in text:
        if i in filters:
            text = text.replace(i, " " + i)

    return text


def create_data(df):
    """
    The function responsible for the creation of data in the said format.
    """
    filepath = "train/train.txt"
    filepath1 = "train/train_backup_file.txt"

    if not os.path.exists("train"):
        os.makedirs("train")
    with open(filepath, "w") as f, open(filepath1, "a") as f1:
        for text, annotation in zip(df.text, df.annotation):
            text = clean(text)
            match_list = []
            for i in annotation:
                a, text_ = matcher(text, i[0])
                match_list.append((a[0][0], a[0][1], i[1]))

            d = mark_sentence(text, match_list)
            for i in d.keys():
                f.writelines(i + " " + d[i] + "\n")
                f1.writelines(i + " " + d[i] + "\n")
            f.writelines("\n")
            f1.writelines("\n")
    return True


def create_data_new(df):
    filepath = "train/train.txt"
    if not os.path.exists("train"):
        os.makedirs("train")
    with open(filepath, "w") as f:
        for text, annotation in zip(df.text, df.annotation):
            text = clean(text)
            text = clean(text)
            split_sent = text.split()
            tags = ["O"] * len(split_sent)
            for i in annotation:
                e_type = i[1]
                ent_val = text[i[2] : i[3]]
                tags[split_sent.index(ent_val.split()[0])] = "B-" + e_type
                split_sent[split_sent.index(ent_val.split()[0])] = (
                    split_sent[split_sent.index(ent_val.split()[0])] + "t"
                )
                # print(tags)
                if len(ent_val.split()) > 1:
                    for ent in ent_val.split()[1:]:
                        tags[split_sent.index(ent)] = "I-" + e_type
                        split_sent[split_sent.index(ent)] = (
                            split_sent[split_sent.index(ent)] + "t"
                        )
            for w, t in zip(text.split(), tags):
                f.writelines(w + " " + t + "\n")
            f.writelines("\n")
    return True


def create_data1(df):
    """
    The function responsible for the creation of data in the said format.
    """
    filepath = "train/train.txt"
    filepath1 = "train/train_backup_file.txt"
    if not os.path.exists("train"):
        os.makedirs("train")
    with open(filepath, "w") as f, open(filepath1, "a") as f1:
        for text, annotation in zip(df.text, df.annotation):
            split_sent = text.split()
            tags = ["O"] * len(split_sent)
            for i in annotation:
                e_type = i[1]
                # print(e_type)
                ent_val = text[i[2] : i[3]]
                # print(i, e_type, ent_val)
                tags[split_sent.index(ent_val.split()[0])] = e_type

            for i in range(len(tags)):
                f.writelines(split_sent[i] + " " + tags[i] + "\n")
                f1.writelines(split_sent[i] + " " + tags[i] + "\n")
            f.writelines("\n")
            f1.writelines("\n")
    return True
