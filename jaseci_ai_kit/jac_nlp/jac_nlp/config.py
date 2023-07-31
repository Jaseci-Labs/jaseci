from .action_configs.summarization_action_config import SUMMARIZATION_ACTION_CONFIG
from .action_configs.bi_enc_action_config import BI_ENC_ACTION_CONFIG
from .action_configs.cl_summer_action_config import CL_SUMMER_ACTION_CONFIG
from .action_configs.sbert_sim_action_config import SBERT_SIM_ACTION_CONFIG
from .action_configs.text_seg_action_config import TEXT_SEG_ACTION_CONFIG
from .action_configs.tfm_ner_action_config import TFM_NER_ACTION_CONFIG
from .action_configs.topic_ext_action_config import TOPIC_EXT_ACTION_CONFIG
from .action_configs.use_enc_action_config import USE_ENC_ACTION_CONFIG
from .action_configs.use_qa_action_config import USE_QA_ACTION_CONFIG
from .action_configs.sentiment_action_config import SENTIMENT_ACTION_CONFIG

ACTION_CONFIGS = {
    "summarization": SUMMARIZATION_ACTION_CONFIG,
    "bi_enc": BI_ENC_ACTION_CONFIG,
    "cl_summer": CL_SUMMER_ACTION_CONFIG,
    "sbert_sim": SBERT_SIM_ACTION_CONFIG,
    "text_seg": TEXT_SEG_ACTION_CONFIG,
    "tfm_ner": TFM_NER_ACTION_CONFIG,
    "topic_ext": TOPIC_EXT_ACTION_CONFIG,
    "use_enc": USE_ENC_ACTION_CONFIG,
    "use_qa": USE_QA_ACTION_CONFIG,
    "sentiment": SENTIMENT_ACTION_CONFIG,
}
