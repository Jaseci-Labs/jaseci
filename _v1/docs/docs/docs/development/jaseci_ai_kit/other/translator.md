---
sidebar_position: 1
title: Translator Module
description: Text Translating with Jaseci.
---

# Translator Module

Module `translator` uses the `mbart-large-50-many-to-many` to perform multilingual translation. It can translate from 50 languages to 50 languages.

## Actions

* `translator` : Module `translator` uses the `mbart-large-50-many-to-many` to perform multilingual translation. It can translate from 50 languages to 50 languages.
  * Alternate name:
  * Input:
    * `text` - Text to be translated. Type: `Union[List[str], str]`
    * `src_lang` - Source language of the text. Type: `str`
    * `tgt_lang` - Target language of the text. Type: `str`
  * Return: Return type of the action is `List[str]`.


## Example Jac Usage:

Example JAC Code to translate text from Hindi to English:

```jac
walker test_translate_hindi_eng {
    can translator.translate;
    report translator.translate("नमस्ते, आप कैसे हैं?", "hi_IN", "en_XX"); # Returns ["Hello, how are you?"]
}
```
Example JAC Code to translate text from English to German:
```jac
walker test_translate_eng_german {
    can translator.translate;
    report translator.translate("Hello, how are you?", "en_XX", "de_DE"); # Returns ["Hallo, wie geht es dir?"]
}
```
For a complete example visit [here](../../../../../tutorials/jaseci_ai_kit/jac_nlp/translator)