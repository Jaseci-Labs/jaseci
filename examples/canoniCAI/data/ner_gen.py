"""
AUTO GENERATE TRAINING FILE FROM NER BASED ON THE UTTERANCE, SLOT TYPE AND VALUE YOU IMPUTTED.
"""

import json

file_name = "flair_ner.json"

file = []

run = True

while run:
    utterance = input(" Enter utterance: ")
    entity_type = input("\n Slot Type: ")
    entity_value = input("\n Slot Value: ")

    start_index = utterance.index(entity_value)
    end_index = utterance.index(entity_value) + len(entity_value)

    data = {
        "context": utterance,
        "entities": [
            {
                "entity_value": entity_value,
                "entity_type": entity_type,
                "start_index": start_index,
                "end_index": end_index,
            }
        ],
    }

    file.append(data)

    continue_to_run = input("\n Do you want to continue (y/n): ")

    if continue_to_run == "n":
        run = False

        with open(file_name, "w") as outfile:
            json.dump(file, outfile)
