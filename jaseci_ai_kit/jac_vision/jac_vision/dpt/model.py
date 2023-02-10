import numpy as np
import torch
from PIL import Image
from transformers import DPTFeatureExtractor, DPTForDepthEstimation


class DPTLarge:
    def __init__(self, device=None, model="dpt-large"):
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = device
        self.feature_extractor = DPTFeatureExtractor.from_pretrained("Intel/dpt-large")
        self.model = DPTForDepthEstimation.from_pretrained("Intel/dpt-large").to(
            self.device
        )

    def estimate(self, image):
        inputs = self.feature_extractor(images=image, return_tensors="pt").to(
            self.device
        )
        outputs = self.model(**inputs)
        predicted_depth = outputs.predicted_depth

        prediction = torch.nn.functional.interpolate(
            predicted_depth.unsqueeze(1),
            size=image.size[::-1],
            mode="bicubic",
            align_corners=False,
        )

        output = prediction.squeeze().cpu().detach().numpy()
        formatted = (output * 255 / np.max(output)).astype("uint8")
        depth = Image.fromarray(formatted)

        return depth

    def estimate_batch(self, images):
        inputs = self.feature_extractor(images=images, return_tensors="pt").to(
            self.device
        )
        outputs = self.model(**inputs)
        predicted_depth = outputs.predicted_depth

        prediction = torch.nn.functional.interpolate(
            predicted_depth.unsqueeze(1),
            size=images[0].size[::-1],
            mode="bicubic",
            align_corners=False,
        )

        print(prediction.shape)
        output = prediction.squeeze().cpu().detach().numpy()
        formatted = (output * 255 / np.max(output)).astype("uint8")
        depth_imgs = [Image.fromarray(formatted[i]) for i in range(len(formatted))]

        del inputs, outputs
        return depth_imgs

    def get_labels(self):
        return self.model.config.id2label.values()
