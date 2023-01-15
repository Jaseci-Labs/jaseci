from .modules.test_module.action_config import TEST_MODULE_ACTION_CONFIG
from .modules.cl_summer.action_config import CL_SUMMER_ACTION_CONFIG
from .modules.encoders.action_config import BI_ENC_ACTION_CONFIG
from .modules.ent_ext.action_config import ENT_EXT_ACTION_CONFIG
from .modules.fast_enc.action_config import FAST_ENC_ACTION_CONFIG
from .modules.pdf_ext.action_config import PDF_EXT_ACTION_CONFIG
from .modules.text_seg.action_config import TEXT_SEG_ACTION_CONFIG
from .modules.tfm_ner.action_config import TFM_NER_ACTION_CONFIG
from .modules.use_enc.action_config import USE_ENC_ACTION_CONFIG
from .modules.use_qa.action_config import USE_QA_ACTION_CONFIG

ACTION_CONFIGS = {
    "test_module": TEST_MODULE_ACTION_CONFIG,
    "cl_summer": CL_SUMMER_ACTION_CONFIG,
    "bi_enc": BI_ENC_ACTION_CONFIG,
    "ent_ext": ENT_EXT_ACTION_CONFIG,
    "fast_enc": FAST_ENC_ACTION_CONFIG,
    "pdf_ext": PDF_EXT_ACTION_CONFIG,
    "text_seg": TEXT_SEG_ACTION_CONFIG,
    "tfm_ner": TFM_NER_ACTION_CONFIG,
    "use_enc": USE_ENC_ACTION_CONFIG,
    "use_qa": USE_QA_ACTION_CONFIG,
}
