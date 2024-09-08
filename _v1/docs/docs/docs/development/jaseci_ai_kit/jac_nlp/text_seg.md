---
sidebar_position: 6
title: Text Segmentation Model
description: Text Segmentation with Jaseci
---

# Text Segmenter (`text_seg`)

`text_seg` Text segmentation is a method of splitting a document into smaller parts, which is usually called segments. It is widely used in text processing. Each segment has its relevant meaning. Those segments categorized as word, sentence, topic, phrase etc. module implemented for the Topical Change Detection in Documents via Embeddings of Long Sequences.

## Actions

* `get_segements`: gets different topics in the context provided, given a threshold
    * Input
        * `text`(String): text the contain the entire context
        * `threshold`(Float): range is between 0-1, make each sentence as segment if, threshold is 1.
    * Returns: List of Sentences that best summarizes the context

* `load_model`: to load the available model for text segmentation
    * Input
        * `model_name`(String): name of the transformer model to load, options are:
            * `wiki`: trained on wikipedia data
            * `legal`: trained on legal documents
    * Returns: "[Model Loaded] : <model_name>"

* **Input data file `text_seg.json`**
    ```json
    {
        "text": "There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude. The King of England was at war with him and had led a great army into Scotland to drive him out of the land. Battle after battle had been fought. Six times Bruce had led his brave little army against his foes and six times his men had been beaten and driven into flight. At last his army was scattered, and he was forced to hide in the woods and in lonely places among the mountains. One rainy day, Bruce lay on the ground under a crude shed listening to the patter of the drops on the roof above him. He was tired and unhappy. He was ready to give up all hope. It seemed to him that there was no use for him to try to do anything more. As he lay thinking, he saw a spider over his head making ready to weave her web. He watched her as she toiled slowly and with great care. Six times she tried to throw her frail thread from one beam to another, and six times it fell short. 'Poor thing,' said Bruce: 'you, too, know what it is to fail. But the spider did not lose hope with the sixth failure. With still more care, she made ready to try for the seventh time. Bruce almost forgot his own troubles as he watched her swing herself out upon the slender line. Would she fail again? No! The thread was carried safely to the beam and fastened there."
    }
    ```
## Example Jac Usage:
```jac
walker text_seg_example {
    has data_file = "text_seg.json";
    has threshold = 0.85;
    can text_seg.get_segments, text_seg.load_model;

    # loading the desired model
    resp_data = text_seg.load_model(model_name='wiki');
    std.out(resp_data);

    # Getting Segments of different topic from text
    data = file.load_json(data_file);
    resp_data = text_seg.get_segments(
        text=data.text,
        threshold=threshold
        );
    std.out(resp_data);
}
```

For a complete example visit [here](../../../../../tutorials/jaseci_ai_kit/jac_nlp/text_seg)