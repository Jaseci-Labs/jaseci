from http.client import ImproperConnectionState
from typing import Any, Dict
import torch
import uuid as uuid_gen
import os
import shutil
from collections import OrderedDict
import json

from .utils import model as model_module
from .utils import process as process_module
from .utils.logger import get_logger
import logging
from .utils.util import deep_update, write_yaml, read_yaml

from .train import train

import warnings

warnings.filterwarnings("ignore")


class InferenceEngine:
    """
    Inference Engine for each user.
    @param: config: Dict
    """

    def __init__(self, config: Dict, uuid=None):
        self.ph_config = config
        self.id = uuid if uuid else str(uuid_gen.uuid4())

        os.makedirs(f"heads/{self.id}", exist_ok=True)
        write_yaml(self.ph_config, f"heads/{self.id}/config.yaml")

        self.logger = get_logger(name=self.id)
        self.logger.addHandler(logging.FileHandler(f"heads/{self.id}/log.txt"))
        self.logger.setLevel(logging.DEBUG)

        self.infer_config = config["Inference"]

        # Building the Model
        model_config = config["Model"]
        self.model = getattr(model_module, model_config["type"])(
            **model_config.get("args", {})
        )

        # Loading the weights
        if self.infer_config["weights"]:
            if not os.path.exists(f"heads/{self.id}/current.pth"):
                shutil.copyfile(
                    self.infer_config["weights"], f"heads/{self.id}/current.pth"
                )
                self.logger.info(
                    "Loading default checkpoint: {} ...".format(
                        self.infer_config["weights"]
                    )
                )

            checkpoint = torch.load(f"heads/{self.id}/current.pth")
            state_dict = checkpoint.get("state_dict", checkpoint)
            model_keys = list(self.model.state_dict().keys())
            if model_keys[0].startswith("model."):
                new_state_dict = OrderedDict()
                for k, v in state_dict.items():
                    name = "model." + k
                    new_state_dict[name] = v
                state_dict = new_state_dict
            self.model.load_state_dict(state_dict)

        # Setting the device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)
        self.model.eval()

        # Get Intermediate Activations
        self.out_activation_layer = self.infer_config.get("out_activation_layer", None)
        if self.out_activation_layer:
            self.activation = {}
            getattr(self.model, self.out_activation_layer).register_forward_hook(
                self.get_activation(self.out_activation_layer)
            )

        # Initialize Pre-processor
        preprocessor_args = self.infer_config["preprocess"].get("args", {})
        if self.infer_config["preprocess"]["type"].startswith("Custom"):
            preprocessor_args["module_name"] = "CustomPreProcessor"
        self.preprocessor = getattr(
            process_module, self.infer_config["preprocess"]["type"]
        )(**preprocessor_args)
        # Initialize Post-processor
        postprocessor_args = self.infer_config["postprocess"].get("args", {})
        if self.infer_config["postprocess"]["type"].startswith("Custom"):
            postprocessor_args["module_name"] = "CustomPostProcessor"
        self.postprocessor = getattr(
            process_module, self.infer_config["postprocess"]["type"]
        )(**postprocessor_args)

    @torch.no_grad()
    def predict(self, data: Any) -> Any:
        self.logger.info("Predict is called")
        data = self.preprocessor.process(data)
        data = data.to(self.device)
        output = self.model(data)
        if self.out_activation_layer:
            output = self.activation[self.out_activation_layer]
        return self.postprocessor.process(output)

    def get_activation(self, name):
        def hook(model, input, output):
            self.activation[name] = output.detach()

        return hook

    def load_weights(self, weights: str) -> None:
        self.logger.info("Loading new weights: {} ...".format(weights))
        checkpoint = torch.load(weights)
        state_dict = checkpoint.get("state_dict", checkpoint)
        self.model.load_state_dict(state_dict)

    def __del__(self):
        del self.model
        torch.cuda.empty_cache()


class InferenceList:
    """
    Parent of Inference Engines. use to manage multiple Inference Engines.
    """

    def __init__(self, config: Dict = None) -> None:  # type: ignore
        self.config = config
        with open("heads/config.yaml", "w") as f:
            json.dump(config, f)
        os.makedirs("heads", exist_ok=True)
        self.ie_list = {}
        self.ph_list = []
        if os.path.exists("heads/ph_list.json"):
            with open("heads/ph_list.json", "r") as f:
                self.ph_list = json.load(f)

    def add(self, config: Dict = None, uuid: str = None) -> str:  # type: ignore
        if self.check(uuid):
            raise ImproperConnectionState(
                f"{self.check(uuid)} Inference Engine already exists. Please use another uuid."
            )
        if config:
            ie = InferenceEngine(config, uuid)
        else:
            ie = InferenceEngine(self.config, uuid)
        self.ie_list[ie.id] = ie
        if not os.path.exists("heads/ph_list.json"):
            with open("heads/ph_list.json", "w") as f:
                json.dump([], f)
        with open("heads/ph_list.json", "r") as f:
            self.ph_list = json.load(f)
            self.ph_list.append(ie.id)
        with open("heads/ph_list.json", "w") as f:
            json.dump(self.ph_list, f)
        return ie.id

    def predict(self, uuid: str, data: Any) -> Any:
        if self.check(uuid):
            return self.ie_list[uuid].predict(data)
        else:
            raise ImproperConnectionState("Inference Engine not found.")

    def train(self, uuid: str, config: Dict = None, auto_update=True) -> None:  # type: ignore
        if self.check(uuid):
            ph_config = self.ie_list[uuid].ph_config
            if config:
                deep_update(ph_config, config)
                write_yaml(ph_config, f"heads/{uuid}/config.yaml")
            resume = (
                f"heads/{uuid}/current.pth"
                if os.path.exists(f"heads/{uuid}/current.pth")
                else None
            )

            run_id = train(
                {
                    "uuid": uuid,
                    "config": f"heads/{uuid}/config.yaml",
                    "resume": resume,
                    "device": None,
                }
            )
            if auto_update:
                self.update_head(uuid, run_id)
        else:
            raise ImproperConnectionState("Inference Engine not found.")

    def update_head(self, uuid: str, run_id: str) -> None:
        if os.path.exists(f"heads/{uuid}/runs/{run_id}/model_best.pth"):
            shutil.copyfile(
                f"heads/{uuid}/runs/{run_id}/model_best.pth",
                f"heads/{uuid}/current.pth",
            )
            self.ie_list[uuid].load_weights(f"heads/{uuid}/current.pth")
        else:
            print(f"Model for {uuid} has not improved. No update.")

    def get_config(self, uuid: str) -> Dict:
        if self.check(uuid):
            return self.ie_list[uuid].ph_config
        else:
            raise ImproperConnectionState("Inference Engine not found.")

    def delete_head(self, uuid: str) -> None:
        if self.check(uuid):
            del self.ie_list[uuid]
            self.ph_list.remove(uuid)
            with open("heads/ph_list.json", "w") as f:
                json.dump(self.ph_list, f)
            shutil.rmtree(f"heads/{uuid}")
        else:
            raise ImproperConnectionState("Inference Engine not found.")

    def load_head(self, uuid: str) -> None:
        config = read_yaml(f"heads/{uuid}/config.yaml")
        self.ie_list[uuid] = InferenceEngine(config, uuid)
        if os.path.exists(f"heads/{uuid}/current.pth"):
            self.ie_list[uuid].load_weights(f"heads/{uuid}/current.pth")

    def check(self, uuid: str) -> bool:
        if uuid in self.ph_list and uuid in self.ie_list:
            return True
        if uuid in self.ph_list:
            self.load_head(uuid)
            return True
        return False
