import utils.model as model_module
import utils.process as process_module
from utils.logger import get_logger
import torch


class InferenceEngine:
    def __init__(self, config):
        self.logger = get_logger('InferenceEngine')

        self.config = config['Inference']

        # Building the Model
        model_config = config['Model']
        if model_config['args']:
            self.model = getattr(model_module, model_config['type'])(
                model_config['args'])
        else:
            self.model = getattr(model_module, model_config['type'])()

        if self.config["weights"]:
            self.logger.info('Loading checkpoint: {} ...'.format(config.resume))
            checkpoint = torch.load(self.config["weights"])
            state_dict = checkpoint['state_dict']
            self.model.load_state_dict(state_dict)

        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.model.to(self.device)
        self.model.eval()

        # Initialize Post-processor
        if self.config['preprocess']['args']:
            self.preprocessor = getattr(process_module, self.config['preprocess']['type'])(
                self.config['preprocess']['args'])
        else:
            self.preprocessor = getattr(process_module, self.config['preprocess']['type'])()
        # Initialize Post-processor
        if self.config['postprocess']['args']:
            self.postprocessor = getattr(process_module, self.config['postprocess']['type'])(
                self.config['postprocess']['args'])
        else:
            self.postprocessor = getattr(process_module, self.config['postprocess']['type'])()

    @torch.no_grad()
    def predict(self, data):
        data = self.preprocessor.process(data)
        data = data.to(self.device)
        output = self.model(data)
        return self.postprocessor.process(output)

    def __del__(self):
        del self.model
        del self.device
        torch.cuda.empty_cache()
