from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from jaseci.jsorc.live_actions import jaseci_action
from typing import Union, List
from fastapi import HTTPException
import traceback

model = None
tokenizer = None


@jaseci_action(act_group=["translator"], allow_remote=True)
def setup():
    global model, tokenizer, supported_languages
    model = MBartForConditionalGeneration.from_pretrained(
        "facebook/mbart-large-50-many-to-many-mmt"
    )
    tokenizer = MBart50TokenizerFast.from_pretrained(
        "facebook/mbart-large-50-many-to-many-mmt"
    )
    supported_languages = list(tokenizer.lang_code_to_id.keys())


setup()


@jaseci_action(act_group=["translator"], allow_remote=True)
def translate(text: Union[str, List[str]], src_lang: str, tgt_lang: str) -> List[str]:
    """
    Translate text from one language to another.

    Args:
        text (Union[str, List[str]]): Text to translate.
        src_lang (str): Source language.
        tgt_lang (str): Target language.

    Returns:
        List[str]: Translated text.
    """
    global model, tokenizer
    try:
        if src_lang not in supported_languages:
            raise ValueError(f"Unsupported source language: {src_lang}")
        if tgt_lang not in supported_languages:
            raise ValueError(f"Unsupported target language: {tgt_lang}")

        if isinstance(text, str):
            text = [text]
        tokenizer.src_lang = src_lang
        forced_bos_token_id = tokenizer.lang_code_to_id[tgt_lang]
        encoded = tokenizer(text, return_tensors="pt")
        generated_tokens = model.generate(
            **encoded,
            forced_bos_token_id=forced_bos_token_id,
        )
        return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["translator"], allow_remote=True)
def get_supported_languages() -> List[str]:
    """
    Get a list of supported languages.

    Returns:
        List[str]: List of supported languages.
    """
    return supported_languages
