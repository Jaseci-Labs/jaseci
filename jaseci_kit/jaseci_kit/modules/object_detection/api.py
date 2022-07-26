from fastapi import FastAPI, Form, File, UploadFile
from typing import List, Optional

import cv2, torch, random, base64, uuid
import numpy as np

app = FastAPI()

colors = [
    tuple([random.randint(0, 255) for _ in range(3)]) for _ in range(100)
]  # for bbox plotting


@app.post("/load_model")
def load_model(
    name: str = Form("last"),
    confidence_threshold: float = Form(0.05),
):

    global model
    global conf

    try:
        conf = confidence_threshold

        model = torch.hub.load(
            "ultralytics/yolov5",
            "custom",
            path="model/" + name + ".pt",
        )
    except:
        return {"message": "Couldn't load model."}

    return {"message": "Model loaded sucessfully."}


@app.post("/detect")
def detect(
    file_list: List[UploadFile] = File(...),
    image_size: Optional[int] = Form(416),
    download_image: Optional[bool] = Form(False),
):

    # confidence threshold
    model.conf = conf

    img_batch = [
        cv2.imdecode(np.fromstring(file.file.read(), np.uint8), cv2.IMREAD_COLOR)
        for file in file_list
    ]

    # create a copy that corrects for cv2.imdecode generating BGR images instead of RGB,
    # using cvtColor instead of [...,::-1] to keep array contiguous in RAM
    img_batch_rgb = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in img_batch]

    results = model(img_batch_rgb, size=image_size)

    json_results = results_to_json(results, model)

    if download_image:
        # server side render the image with bounding boxes
        for idx, (img, bbox_list) in enumerate(zip(img_batch, json_results)):
            for bbox in bbox_list:
                label = f'{bbox["class_name"]} {bbox["confidence"]:.2f}'
                plot_one_box(
                    bbox["bbox"],
                    img,
                    label=label,
                    color=colors[int(bbox["class"])],
                    line_thickness=3,
                )

            payload = {"image_base64": base64EncodeImage(img)}

            with open("images/" + str(uuid.uuid4()) + ".jpg", "wb") as file:
                file.write(base64.b64decode(base64EncodeImage(img)))

            json_results[idx].append(payload)

    encoded_json_results = str(json_results).replace("'", r'"')
    return encoded_json_results


##############################################
# --------------Helper Functions---------------
##############################################


def results_to_json(results, model):
    """Converts yolo model output to json (list of list of dicts)"""
    return [
        [
            {
                "class": int(pred[5]),
                "class_name": model.model.names[int(pred[5])],
                "bbox": [
                    int(x) for x in pred[:4].tolist()
                ],  # convert bbox results to int from float
                "confidence": float(pred[4]),
            }
            for pred in result
        ]
        for result in results.xyxy
    ]


def plot_one_box(x, im, color=(128, 128, 128), label=None, line_thickness=3):
    # Directly copied from: https://github.com/ultralytics/yolov5/blob/cd540d8625bba8a05329ede3522046ee53eb349d/utils/plots.py
    # Plots one bounding box on image 'im' using OpenCV
    assert (
        im.data.contiguous
    ), "Image not contiguous. Apply np.ascontiguousarray(im) to plot_on_box() input image."
    tl = (
        line_thickness or round(0.002 * (im.shape[0] + im.shape[1]) / 2) + 1
    )  # line/font thickness
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(im, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(im, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(
            im,
            label,
            (c1[0], c1[1] - 2),
            0,
            tl / 3,
            [225, 255, 255],
            thickness=tf,
            lineType=cv2.LINE_AA,
        )


def base64EncodeImage(img):
    """Takes an input image and returns a base64 encoded string representation of that image (jpg format)"""
    _, im_arr = cv2.imencode(".jpg", img)
    im_b64 = base64.b64encode(im_arr.tobytes()).decode("utf-8")

    return im_b64
