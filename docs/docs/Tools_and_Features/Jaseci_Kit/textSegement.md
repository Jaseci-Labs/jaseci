
# Text Segmenter 
`text_seg` module implemented for the Topical Change Detection in Documents via Embeddings of Long Sequences.
* `get_segements`: gets different topics in the context provided, given a threshold 


To load the Text Segmenter run :

```
actions load module jaseci_ai_kit.text_seg
```

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

#### Example Jac Usage:
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
    resp_data = text_seg.get_segments(text=data.text,
    threshold=threshold);
    std.out(resp_data);
}
```