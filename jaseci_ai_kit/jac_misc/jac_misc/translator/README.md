# **Translator (`translator`)**

Module `translator` uses the `mbart-large-50-many-to-many` to perform multilingual translation. It can translate from 50 languages to 50 languages.

1. Import [`translator`](#1-import-translator-module-in-jac) module in jac
2. [Translate](#2-translate)

# **Walk through**

## **1. Import Translator (`translator`) module in jac**
1. For executing jaseci Open terminal and run follow command.
    ```bash
    jsctl -m
    ```
2.  Load translator module in jac
    ```bash
    jsctl> actions load module jac_misc.translator
    ```


## **2. Translate **

Following are the parameters for the action `translator.translate`:
* `text` - Text to be translated. Type: `Union[List[str], str]`
* `src_lang` - Source language of the text. Type: `str`
* `tgt_lang` - Target language of the text. Type: `str`

Return type of the action is `List[str]`.

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

Action `translator.translate` can also translate multiple texts at once. For that, pass a list of texts to the action.
# **Supported Languages**

'ar_AR', 'cs_CZ', 'de_DE', 'en_XX', 'es_XX', 'et_EE', 'fi_FI', 'fr_XX', 'gu_IN', 'hi_IN', 'it_IT', 'ja_XX',
'kk_KZ', 'ko_KR', 'lt_LT', 'lv_LV', 'my_MM', 'ne_NP', 'nl_XX', 'ro_RO', 'ru_RU', 'si_LK', 'tr_TR', 'vi_VN',
'zh_CN', 'af_ZA', 'az_AZ', 'bn_IN', 'fa_IR', 'he_IL', 'hr_HR', 'id_ID', 'ka_GE', 'km_KH', 'mk_MK', 'ml_IN',
'mn_MN', 'mr_IN', 'pl_PL', 'ps_AF', 'pt_XX', 'sv_SE', 'sw_KE', 'ta_IN', 'te_IN', 'th_TH', 'tl_XX', 'uk_UA',
'ur_PK', 'xh_ZA', 'gl_ES', 'sl_SI'

you can the supporter action `translator.get_supported_languages` to get the list of supported languages.

# **References**
* [Multilingual Denoising Pre-training for Neural Machine Translation](https://arxiv.org/abs/2001.08210) by Yinhan Liu, Jiatao Gu, Naman Goyal, Xian Li, Sergey Edunov Marjan Ghazvininejad, Mike Lewis, Luke Zettlemoyer.
* [Huggingface MBart Docs](https://huggingface.co/transformers/model_doc/mbart.html)