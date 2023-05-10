---
title: Text Paraphrasing
---

# Text Paraphrasing Model (`paraphraser`)

Module `paraphraser` implemented for paraphrasing the input sentence. Paraphrasing is the act of expressing the same meaning of a written or spoken text using different words, without changing the original message or altering the main ideas. Paraphrasing is often used to restate a passage in a simpler or more concise way, to avoid plagiarism, or to clarify complex ideas. It involves understanding the original text, analyzing its key points, and rewording it in your own words while maintaining the original meaning. Effective paraphrasing requires good language skills, attention to context, and a clear understanding of the purpose of the text.


# **Walk through**

## **1. Import text cluster (`paraphraser`) module in jac**
1. For executing jaseci open terminal and run following command.
    ```
    jsctl -m
    ```
2.  Load `paraphraser` module in jac shell session
    ```
    actions load module jac_nlp.paraphraser
    ```

## **2. Paraphrase Text**

Use `paraphraser.paraphrase` action to get a list of paraphrased versions of given input text.

- `text` - (string) Input text phrase.

```jac
walker init{
    can paraphraser.paraphrase;

    report paraphraser.paraphrase("Yiping Kang is inviting you to a scheduled Zoom meeting");
}
```

Expected output:

```json
{
  "success": true,
  "report": [
    [
      "Yiping Kang is inviting you to a scheduled Zoom meeting. Yiping Kang is inviting you to a scheduled Zoom meeting.",
      "Yiping Kang invites you to Zoom meeting. Yiping Kang is inviting you to a scheduled Zoom meeting.",
      "Yiping Kang is inviting you to a scheduled Zoom meeting. Yiping Kang is inviting you to a scheduled Zoom meeting.",
      "Yiping Kang invites you for Zoom meeting on Wednesday, November 15th. Yiping Kang is inviting you to a scheduled Zoom meeting on Wednesday, November 15th.",
      "Yiping Kang is inviting you to a scheduled Zoom meeting. Zoom meeting is scheduled for Monday, May 15th, 2016."
    ]
  ],
  "final_node": "urn:uuid:63f04ac7-a4de-4388-81ee-75e4313f9f94",
  "yielded": false
}
```