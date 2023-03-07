from transformers import AutoFeatureExtractor, AutoModelForObjectDetection
import torch


class YolosDetector:
    def __init__(self, device=None):
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = device

        self.feature_extractor = AutoFeatureExtractor.from_pretrained(
            "hustvl/yolos-tiny"
        )
        self.model = AutoModelForObjectDetection.from_pretrained(
            "hustvl/yolos-tiny"
        ).to(self.device)

    def detect(self, image, threshold=0.5):
        inputs = self.feature_extractor(images=image, return_tensors="pt").to(
            self.device
        )
        outputs = self.model(**inputs)

        target_sizes = torch.tensor([image.size[::-1]]).to(self.device)
        results = self.feature_extractor.post_process_object_detection(
            outputs, threshold=threshold, target_sizes=target_sizes
        )[0]

        detections = []
        for score, label, box in zip(
            results["scores"], results["labels"], results["boxes"]
        ):
            box = [round(i, 2) for i in box.tolist()]
            labelname = self.model.config.id2label[label.item()]
            score = round(score.item(), 3)
            detections.append({"label": labelname, "score": score, "box": box})

        return detections

    def detect_batch(self, images, threshold=0.5):
        inputs = self.feature_extractor(images=images, return_tensors="pt").to(
            self.device
        )
        outputs = self.model(**inputs)

        target_sizes = torch.tensor([image.size[::-1] for image in images])
        results = self.feature_extractor.post_process_object_detection(
            outputs, threshold=threshold, target_sizes=target_sizes.to(self.device)
        )

        batch_detections = []
        for i, image in enumerate(images):
            detections = []
            for score, label, box in zip(
                results[i]["scores"], results[i]["labels"], results[i]["boxes"]
            ):
                box = [round(i, 2) for i in box.tolist()]
                labelname = self.model.config.id2label[label.item()]  # type: ignore
                score = round(score.item(), 3)
                detections.append({"label": labelname, "score": score, "box": box})
            batch_detections.append(detections)

        del inputs, outputs, results
        return batch_detections

    def get_labels(self):
        return self.model.config.id2label.values()
