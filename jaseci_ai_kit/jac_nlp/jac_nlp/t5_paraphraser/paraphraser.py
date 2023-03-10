from fastapi import HTTPException
from jaseci.actions.live_actions import jaseci_action
from parrot import Parrot
from typing import List
import warnings

warnings.filterwarnings("ignore")
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)


@jaseci_action(act_group=["t5_paraphraser"], allow_remote=True)
def paraphrase_text(phrases: List):
    para_phrases = {}
    try:
        for phrase in phrases:
            para_phrases[phrase] = parrot.augment(
                input_phrase=phrase, max_return_phrases=10, do_diverse=True
            )
        return para_phrases

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
