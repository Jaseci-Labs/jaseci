---
sidebar_position: 9
title: Paraphraser Model
description: Text Paraphrasing with Jaseci
---

# Paraphraser Model (`paraphraser`)

Module `paraphraser` implemented for paraphrasing the input sentence. Paraphrasing is the act of expressing the same meaning of a written or spoken text using different words, without changing the original message or altering the main ideas. Paraphrasing is often used to restate a passage in a simpler or more concise way, to avoid plagiarism, or to clarify complex ideas. It involves understanding the original text, analyzing its key points, and rewording it in your own words while maintaining the original meaning. Effective paraphrasing requires good language skills, attention to context, and a clear understanding of the purpose of the text.

## Actions

Module `paraphraser` implemented for paraphrasing the given input text.

- `text` - (Strings) Input text phrases.

## Example Jac Usage:

```jac
walker init{
    can paraphraser.paraphrase;

    has text = "Yiping Kang is inviting you to a scheduled Zoom meeting";

    report paraphraser.paraphrase(text=text);
}
```

For a complete example visit [here](../../../../../tutorials/jaseci_ai_kit/jac_nlp/paraphraser)