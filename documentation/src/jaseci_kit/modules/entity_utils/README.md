# Entity Extraction / Recognition

Named entity recognition (NER) is the process of categroizing and identifying informational entities in text. Jaseci provides the following NER engines: 


| Module                | Model Name      | Type           | Status       | Description                                                       | Resources                                                                                               |
| --------------------- | --------------- | -------------- | ------------ | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| [`ent_ext`](flair_ner/README.md) | Flair NER                      | Training req.  | Ready        | Entity extraction using the FLAIR NER framework                   |           [Documentation](flair_ner/README.md)                                                                                              |
| [`tfm_ner`](flair_ner/README.md)             | Transformer NER |  Training req.  | Ready        | Token classification on Transformer models, can be used for NER   | [Documentation](tfm_ner/README.md) [Huggingface](https://huggingface.co/docs/transformers/tasks/token_classification#token-classification) 
| `lstm_ner`            | LSTM NER        |        Training Required                                                | Experimental | Entity extraction/Slot filling via Long-short Term Memory Network |                                                          
