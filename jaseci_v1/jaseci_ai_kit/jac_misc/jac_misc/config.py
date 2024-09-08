from .action_configs.pdf_ext_action_config import PDF_EXT_ACTION_CONFIG
from .action_configs.cluster_action_config import CLUSTER_ACTION_CONFIG
from .action_configs.example_module_action_config import EXAMPLE_MODULE_ACTION_CONFIG
from .action_configs.forecast_action_config import FORECAST_ACTION_CONFIG

ACTION_CONFIGS = {
    "pdf_ext": PDF_EXT_ACTION_CONFIG,
    "cluster": CLUSTER_ACTION_CONFIG,
    "forecast": FORECAST_ACTION_CONFIG,
    "example_module": EXAMPLE_MODULE_ACTION_CONFIG,
}
