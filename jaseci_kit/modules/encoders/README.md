# Encoders

Text encoding is a process to convert meaningful text into number / vector representation so as to preserve the context and relationship between words and sentences, such that a machine can understand the pattern associated in any text and can make out the context of sentences.

Jaseci Kit provides the following optimized text encoders:

- [USE Encoder](use_enc/README.md)
- [USE QA](use_qa/README.md)
- [FastText](fast_enc/README.md)
- [Bi-Encoder](bi_enc/README.md)

## Encoders
| Module      | Model Name    | Type                    | Status       | Description                                                 | Resources                                 |
| ----------- | ------------- | ----------------------- | ------------ | ----------------------------------------------------------- | ----------------------------------------- |
| `use_enc`   | USE Encoder   |    Zero-shot  |  Ready        | Sentence-level embedding pre-trained on general text corpus | [Documentation](use_enc/README.md) [Paper](https://arxiv.org/abs/1803.11175) |
| `use_qa`    | USE QA                    | Zero-shot               | Ready        | Sentence-level embedding pre-trained on Q&A data corpus     | [Documentation](use_qa/README.md) [Paper](https://arxiv.org/abs/1803.11175) |
| `fast_enc`  | FastText      | Training required           | Ready        | FastText Text Classifier                                    | [Documentation](fast_enc/README.md)  [Paper](https://arxiv.org/abs/1712.09405) |
| `bi_enc`    | Bi-encoder         | Training required / Zero-shot | Ready        | Dual sentence-level encoders                                | [Documentation](bi_enc/README.md)  [Paper](https://arxiv.org/abs/1803.11175) |
