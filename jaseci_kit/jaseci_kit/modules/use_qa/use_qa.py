import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_text  # noqa
from jaseci.actions.live_actions import jaseci_action
from typing import Union


module = hub.load(
    "https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3"
)


@jaseci_action(act_group=["use"], aliases=["enc_question"], allow_remote=True)
def question_encode(question: Union[str, list]):
    if isinstance(question, list):
        return (
            module.signatures["question_encoder"](tf.constant(question))["outputs"]
            .numpy()
            .tolist()
        )
    elif isinstance(question, str):
        return (
            module.signatures["question_encoder"](tf.constant([question]))["outputs"]
            .numpy()
            .tolist()
        )


@jaseci_action(act_group=["use"], aliases=["enc_answer"], allow_remote=True)
def answer_encode(answer: Union[str, list], context: Union[str, list] = None):
    if context is None:
        context = answer
    if isinstance(answer, list):
        return (
            module.signatures["response_encoder"](
                input=tf.constant(answer), context=tf.constant(context)
            )["outputs"]
            .numpy()
            .tolist()
        )
    elif isinstance(answer, str):
        return (
            module.signatures["response_encoder"](
                input=tf.constant([answer]), context=tf.constant([context])
            )["outputs"]
            .numpy()
            .tolist()
        )


@jaseci_action(act_group=["use"], allow_remote=True)
def cos_sim_score(q_emb: list, a_emb: list):
    norm = np.linalg.norm
    return np.dot(q_emb, a_emb) / (norm(q_emb) * norm(a_emb))


@jaseci_action(act_group=["use"], aliases=["qa_score"], allow_remote=True)
def dist_score(q_emb: list, a_emb: list):
    return np.inner(q_emb, a_emb).tolist()


@jaseci_action(act_group=["use"], allow_remote=True)
def question_similarity(text1: str, text2: str):
    enc_a = np.squeeze(np.asarray(question_encode(text1)))
    enc_b = np.squeeze(np.asarray(question_encode(text2)))
    return cos_sim_score(list(enc_a), list(enc_b))


@jaseci_action(act_group=["use"], allow_remote=True)
def question_classify(text: str, classes: list):
    text_emb = np.squeeze(np.asarray(question_encode(text)))
    ret = {"match": "", "match_idx": -1, "scores": []}
    for i in classes:
        i_emb = np.squeeze(np.asarray(question_encode(i))) if isinstance(i, str) else i
        ret["scores"].append(cos_sim_score(text_emb, i_emb))
    top_hit = ret["scores"].index(max(ret["scores"]))
    ret["match_idx"] = top_hit
    ret["match"] = (
        classes[top_hit] if isinstance(classes[top_hit], str) else "[embedded value]"
    )
    return ret


@jaseci_action(act_group=["use"], allow_remote=True)
def answer_similarity(text1: str, text2: str):
    enc_a = np.squeeze(np.asarray(answer_encode(text1)))
    enc_b = np.squeeze(np.asarray(answer_encode(text2)))
    return cos_sim_score(list(enc_a), list(enc_b))


@jaseci_action(act_group=["use"], allow_remote=True)
def answer_classify(text: str, classes: list):
    text_emb = np.squeeze(np.asarray(answer_encode(text)))
    ret = {"match": "", "match_idx": -1, "scores": []}
    for i in classes:
        i_emb = np.squeeze(np.asarray(answer_encode(i))) if isinstance(i, str) else i
        ret["scores"].append(cos_sim_score(text_emb, i_emb))
    top_hit = ret["scores"].index(max(ret["scores"]))
    ret["match_idx"] = top_hit
    ret["match"] = (
        classes[top_hit] if isinstance(classes[top_hit], str) else "[embedded value]"
    )
    return ret


@jaseci_action(act_group=["use"], allow_remote=True)
def qa_similarity(text1: str, text2: str):
    enc_a = np.squeeze(np.asarray(question_encode(text1)))
    enc_b = np.squeeze(np.asarray(answer_encode(text2)))
    return cos_sim_score(list(enc_a), list(enc_b))


@jaseci_action(act_group=["use"], allow_remote=True)
def qa_classify(text: str, classes: list):
    text_emb = np.squeeze(np.asarray(question_encode(text)))
    ret = {"match": "", "match_idx": -1, "scores": []}
    for i in classes:
        i_emb = np.squeeze(np.asarray(answer_encode(i))) if isinstance(i, str) else i
        ret["scores"].append(cos_sim_score(text_emb, i_emb))
    top_hit = ret["scores"].index(max(ret["scores"]))
    ret["match_idx"] = top_hit
    ret["match"] = (
        classes[top_hit] if isinstance(classes[top_hit], str) else "[embedded value]"
    )
    return ret


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
