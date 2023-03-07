from transformers import DetrImageProcessor, DetrForObjectDetection
import torch


class DetrDetector:
    def __init__(self, device=None, model="detr-resnet-50"):
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = device
        self.processor = DetrImageProcessor.from_pretrained(f"facebook/{model}")
        self.model = DetrForObjectDetection.from_pretrained(
            "facebook/detr-resnet-50"
        ).to(self.device)

    def detect(self, image, threshold=0.5):
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        outputs = self.model(**inputs)

        target_sizes = torch.tensor([image.size[::-1]])
        results = self.processor.post_process_object_detection(
            outputs, threshold=threshold, target_sizes=target_sizes.to(self.device)
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
        inputs = self.processor(images=images, return_tensors="pt").to(self.device)
        outputs = self.model(**inputs)

        target_sizes = torch.tensor([image.size[::-1] for image in images])
        results = self.processor.post_process_object_detection(
            outputs, threshold=threshold, target_sizes=target_sizes.to(self.device)
        )

        batch_detections = []
        for i, image in enumerate(images):
            detections = []
            for score, label, box in zip(
                results[i]["scores"], results[i]["labels"], results[i]["boxes"]
            ):
                box = [round(i, 2) for i in box.tolist()]
                labelname = self.model.config.id2label[label.item()]
                score = round(score.item(), 3)
                detections.append({"label": labelname, "score": score, "box": box})
            batch_detections.append(detections)

        del inputs, outputs, results
        return batch_detections

    def get_labels(self):
        return self.model.config.id2label.values()
