from .bart_sum.action_config import BART_SUM_ACTION_CONFIG
from .bi_enc.action_config import BI_ENC_ACTION_CONFIG
from .bi_ner.action_config import BI_NER_ACTION_CONFIG
from .cl_summer.action_config import CL_SUMMER_ACTION_CONFIG
from .ent_ext.action_config import ENT_EXT_ACTION_CONFIG
from .fast_enc.action_config import FAST_ENC_ACTION_CONFIG
from .sbert_sim.action_config import SBERT_SIM_ACTION_CONFIG
from .text_seg.action_config import TEXT_SEG_ACTION_CONFIG
from .tfm_ner.action_config import TFM_NER_ACTION_CONFIG
from .topic_ext.action_config import TOPIC_EXT_ACTION_CONFIG
from .use_enc.action_config import USE_ENC_ACTION_CONFIG
from .use_qa.action_config import USE_QA_ACTION_CONFIG
from .zs_classifier.action_config import ZS_CLASSIFIER_ACTION_CONFIG

ACTION_CONFIGS = {
    "bart_sum": BART_SUM_ACTION_CONFIG,
    "bi_enc": BI_ENC_ACTION_CONFIG,
    "bi_ner": BI_NER_ACTION_CONFIG,
    "cl_summer": CL_SUMMER_ACTION_CONFIG,
    "ent_ext": ENT_EXT_ACTION_CONFIG,
    "fast_enc": FAST_ENC_ACTION_CONFIG,
    "sbert_sim": SBERT_SIM_ACTION_CONFIG,
    "text_seg": TEXT_SEG_ACTION_CONFIG,
    "tfm_ner": TFM_NER_ACTION_CONFIG,
    "topic_ext": TOPIC_EXT_ACTION_CONFIG,
    "use_enc": USE_ENC_ACTION_CONFIG,
    "use_qa": USE_QA_ACTION_CONFIG,
    "zs_classifier": ZS_CLASSIFIER_ACTION_CONFIG,
}
