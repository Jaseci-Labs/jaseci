from jaseci.svc.actions_optimizer.configs.bi_enc_action_config import (
    BI_ENC_ACTION_CONFIG,
)
from jaseci.svc.actions_optimizer.configs.cl_summer_action_config import (
    CL_SUMMER_ACTION_CONFIG,
)
from jaseci.svc.actions_optimizer.configs.ent_ext_action_config import (
    ENT_EXT_ACTION_CONFIG,
)
from jaseci.svc.actions_optimizer.configs.fast_enc_action_config import (
    FAST_ENC_ACTION_CONFIG,
)
from jaseci.svc.actions_optimizer.configs.pdf_ext_action_config import (
    PDF_EXT_ACTION_CONFIG,
)
from jaseci.svc.actions_optimizer.configs.text_seg_action_config import (
    TEXT_SEG_ACTION_CONFIG,
)
from jaseci.svc.actions_optimizer.configs.tfm_ner_action_config import (
    TFM_NER_ACTION_CONFIG,
)
from jaseci.svc.actions_optimizer.configs.use_enc_action_config import (
    USE_ENC_ACTION_CONFIG,
)
from jaseci.svc.actions_optimizer.configs.use_qa_action_config import (
    USE_QA_ACTION_CONFIG,
)
from jaseci.svc.actions_optimizer.configs.test_module_action_config import (
    TEST_MODULE_ACTION_CONFIG,
)

ACTION_CONFIGS = {
    "use_enc": USE_ENC_ACTION_CONFIG,
    "use_qa": USE_QA_ACTION_CONFIG,
    "bi_enc": BI_ENC_ACTION_CONFIG,
    "tfm_ner": TFM_NER_ACTION_CONFIG,
    "cl_summer": CL_SUMMER_ACTION_CONFIG,
    "ent_ext": ENT_EXT_ACTION_CONFIG,
    "text_seg": TEXT_SEG_ACTION_CONFIG,
    "fast_enc": FAST_ENC_ACTION_CONFIG,
    "pdf_ext": PDF_EXT_ACTION_CONFIG,
    "test_module": TEST_MODULE_ACTION_CONFIG,
}
