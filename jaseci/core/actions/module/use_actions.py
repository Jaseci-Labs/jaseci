from jac_api.apps import JacApiConfig


def enc_question(param_list):
    return JacApiConfig.USE.question_encode(param_list[0])


def enc_answer(param_list):
    return JacApiConfig.USE.answer_encode(param_list[0])


def qa_score(param_list):
    return JacApiConfig.USE.qa_score(param_list[0], param_list[1])
