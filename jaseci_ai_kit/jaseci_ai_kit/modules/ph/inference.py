from http.client import ImproperConnectionState
from typing import Any, Dict
import torch
import uuid as uuid_gen

from .utils import model as model_module
from .utils import process as process_module
from .utils.logger import get_logger

import warnings

warnings.filterwarnings("ignore")


class InferenceEngine:
    """
    Inference Engine for each user.
    @param: config: Dict
    """

    def __init__(self, config: Dict, uuid: str = None):
        self.id = uuid if uuid else str(uuid_gen.uuid4())
        self.logger = get_logger(f"Personalized Header {self.id}")

        self.infer_config = config["Inference"]

        # Building the Model
        model_config = config["Model"]
        self.model = getattr(model_module, model_config["type"])(
            **model_config.get("args", {})
        )

        # Loading the weights
        if self.infer_config["weights"]:
            self.logger.info(
                "Loading checkpoint: {} ...".format(self.infer_config["weights"])
            )
            checkpoint = torch.load(self.infer_config["weights"])
            state_dict = checkpoint["state_dict"]
            self.model.load_state_dict(state_dict)

        # Setting the device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)
        self.model.eval()

        # Initialize Pre-processor
        self.preprocessor = getattr(
            process_module, self.infer_config["preprocess"]["type"]
        )(**self.infer_config["preprocess"].get("args", {}))
        # Initialize Post-processor
        self.postprocessor = getattr(
            process_module, self.infer_config["postprocess"]["type"]
        )(**self.infer_config["postprocess"].get("args", {}))

    @torch.no_grad()
    def predict(self, data: Any) -> Any:
        data = self.preprocessor.process(data)
        data = data.to(self.device)
        output = self.model(data)
        return self.postprocessor.process(output)

    def load_weights(self, weights: str) -> None:
        self.logger.info("Loading new weights: {} ...".format(weights))
        checkpoint = torch.load(weights)
        state_dict = checkpoint["state_dict"]
        self.model.load_state_dict(state_dict)

    def __del__(self):
        del self.model
        del self.device
        torch.cuda.empty_cache()


class InferenceList:
    """
    Parent of Inference Engines. use to manage multiple Inference Engines.
    """

    def __init__(self, config: Dict = None) -> None:
        self.config = config
        self.ie_list = {}

    def add(self, config: Dict = None, uuid: str = None) -> None:
        if self.check(uuid):
            raise ImproperConnectionState(
                f"{self.check(uuid)} Inference Engine already exists. Please use another uuid."
            )
        if config:
            ie = InferenceEngine(config, uuid)
        else:
            ie = InferenceEngine(self.config, uuid)
        self.ie_list[ie.id] = ie
        return ie.id

    def predict(self, uuid: str, data: Any) -> Any:
        if self.check(uuid):
            return self.ie_list[uuid].predict(data)
        else:
            raise ImproperConnectionState("Inference Engine not found.")

    def load_weights(self, uuid: str, weights: str) -> None:
        if uuid in self.ie_list:
            self.ie_list[uuid].load_weights(weights)
        else:
            raise ImproperConnectionState("Inference Engine not found.")

    def check(self, uuid: str) -> bool:
        return uuid in self.ie_list
