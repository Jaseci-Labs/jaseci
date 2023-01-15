



#  **ZeroShot Classfier (`zs_classifier`)**
**`zs_classifier`** is a zeroshot text classification module build on top of flair library. It uses `tars-base` model for text classification

This tutorial shows you how to import and use `zs_classifier` with jac code.


1. Import [ZS Classifier](#1-import-zeroshot-classfierzsclassifier-module-in-jac) module in jac
2. ZeroShot [Predictions](#2-zeroshot-predictions)


## **Walk through**

### **1. Import `ZeroShot Classfier(zs_classifier)` module in jac**
1. Open terminal and run jaseci by cmd
    > jsctl -m
2. Load `zs_classifier` module in jac by cmd
    > actions load module jaseci_ai_kit.zs_classifier
### **2. ZeroShot Predictions** 
* **Creating  a Jac Walker (`predict_zs`)**
    1. Create a file by name `zs_classifier.jac`
    2. Create `predict_zs` walker
        ```jac
        walker predict_zs{
                can zs_classifier.classify;
                report zs_classifier.classify(text="I am so glad you liked it", classes=["happy","sad"]);
            }

        ```

        **Parameter details**
        * `classify`: will be used to train the Bi-NER on custom data
            * Input:
                * `text` (str or List(str)): it can be string or list of string 
                * `classes` (List): list of classes that text needs to be classified
            * Returns: list of classes with the confidence score for each

* **Steps for running `zs_classifier.jac` program**

    3. Build `zs_classifier.jac` by run cmd
        > jac build zs_classifier.jac
    4. Activate sentinal by run cmd
        > sentinel set -snt active:sentinel -mode ir zs_classifier.jir
    5. Calling walker `predict_zs` with `default parameter`
        > walker run predict_zs </br>

    **Expected output**
    ```
    [
        {
            "I am so glad you liked it": [
                {
                    "value": "happy",
                    "confidence": 0.8714166879653931
                }
            ]
        }
    ]
    ```