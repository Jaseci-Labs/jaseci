from datasets import Dataset


def create_dataset(tdata):
    data = {
        "id": [],
        "tokens": [],
        "ner_tags": []
        }
    ind = 1
    for i in tdata:
        text = i['text'].replace(',', ' ')
        text = text.replace("'", " ")
        text = text.replace('"', ' ')
        text = text.replace('(', ' ')
        text = text.replace(')', ' ')
        text = text.replace('<', ' ')
        text = text.replace('>', ' ')
        tokens = text.split()
        ents = ['O']*len(tokens)
        for ent in i['entity']:
            w = text[int(ent['start_index']):int(ent['end_index'])]
            c = 0
            for e in w.split():
                try:
                    if c == 0:
                        ents[tokens.index(e)] = "B-"+ent['entity']
                        c += 1
                    else:
                        ents[tokens.index(e)] = "I-"+ent['entity']
                except Exception as e:
                    # print(text)
                    print(str(e), end=' ')
        data['id'].append(str(ind))
        data['tokens'].append(tokens)
        data['ner_tags'].append(ents)
        ind += 1

    # convertint labels
    lst = []
    for ls in data['ner_tags']:
        lst += ls
    label_name = sorted(list(set(lst)), reverse=True)
    print("*************************", label_name)

    id2label = {str(i): label for i, label in enumerate(label_name)}
    label2id = {v: k for k, v in id2label.items()}

    for i in range(len(data['ner_tags'])):
        data['ner_tags'][i] = [int(label2id[k]) for k in data['ner_tags'][i]]

    dataset = Dataset.from_dict(data)
    return dataset, label_name
