# Available Encoders in Jaseci

This document provides a list of encoders available with their respective action API

| Module          | Model Name                 | Type                 | Embedding Action                                 |
| --------------- | -------------------------- | -------------------- | ------------------------------------------------ | 
| `use_enc`       | USE Encoder                | Zero-shot            | use_enc.encode                                   |
| `use_qa`        | USE QA                     | Zero-shot            | use_qa.question_encode / use_qa.answer_encode    |
| `zs_classifier` | Tars-Base Text Classifier  | Zero-shot            | zs_classifier.get_embeddings                     | 
| `sbert_sim`     | Sentence Bert              | Zero-shot/Trainable  | sbert_sim.getembeddings                          |
| `bi_enc`        | Bi-encoder                 | Zero-shot/Trainable  | bi_enc.get_candidate_emb / bi_enc.get_context_emb|
