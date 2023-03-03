# **T5 ParaPhraser (`t5_phraser`)**

Module `t5_phraser` uses the `t5` to a re-word a corpus of text.


# **Walk through**

##Prerequisites

1. System Memory >= 16GB
2. Install Parrot
```bash
pip3 install git+https://github.com/PrithivirajDamodaran/Parrot_Paraphraser.git
```

## **1. Import T5 ParaPhraser (`t5_phraser`) module in jac**
1. For executing jaseci Open terminal and run follow command.
    ```
    jsctl -m
    ```
2.  Load whisper module in jac
    ```
    actions load module jac_nlp.t5_phraser
    ```


## Paraphrase**

Following are the parameters of the action.
* `phrases` - Spoken Language in the Corpus of Text. Type: Type: `list` Default: `en`

Return type of the action is `object`.

```jac


walker paraphrase_text {
    can t5_phraser.paraphrase_text;
    report t5_phraser.paraphrase_text(["Yiping Kang is inviting you to a scheduled Zoom meeting."]);
}
```