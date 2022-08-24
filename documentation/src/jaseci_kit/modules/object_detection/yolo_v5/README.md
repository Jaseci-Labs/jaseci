# YoloV5

###  Yolo V5 (`yolov5`)
 YOLOv5 `yolov5`  is a family of object detection architectures and models pretrained on the COCO dataset, and represents Ultralytics open-source research into future vision AI methods, incorporating lessons learned and best practices evolved over thousands of hours of research and development.
 
 * `load_model`: Allows you to load the yolov5 pytorch model.
    * Input: 
        * `name` (string) (required): the name of the trained model. 
        * `confidence_threshold` (integer) (optional): is a number between 0 and 1 that represents the likelihood that the output of the Machine Learning model is correct and will satisfy a user's request.
    * Return : Message whether the model was sucessfully loaded or not.
    * Note: Before loading the model (weights) need to be in a specific location at `object_detection/yolov5/runs/train/exp/weights`, with a specific file suffix/type (*.pt)
* `detect`: Based on the image(s) provided by the user it will try to predict where an object alongside with it's label is on the each attached image(s).
    * Input:  
        * `file_list` (files) (required): the image files you want the model to detect objects location.
        * `image_size` (integer) (optional): The inference size of the image(s) attached.
        * `download_image` (boolean) (optional): Whether or not you want the image(s) to be returned to the current API.
    * Return: The class (labels) it picked up from image, Bounding Box Coordinates (bbox) where the object was detected, confidence ( score ) and image in base64 format.


### How to create an image based on the image_bas64 string
In `api.py` there is a function called `base64EncodeImage` this is what converts the image to image arrays then into string.

```
def base64EncodeImage(img):
    """Takes an input image and returns a base64 encoded string representation of that image (jpg format)"""
    _, im_arr = cv2.imencode(".jpg", img)
    im_b64 = base64.b64encode(im_arr.tobytes()).decode("utf-8")

    return im_b64

```

### How it supports multiple images
For the `/detect` endpoint it accepts an array of files and the data have to be send through a multipart or formdata or else it won't work, which will be later encoded, processed and then returned to the user.
