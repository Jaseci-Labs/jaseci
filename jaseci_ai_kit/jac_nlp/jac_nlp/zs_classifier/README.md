#  **ZeroShot Classfier (`zs_classifier`)**
**`zs_classifier`** is a zeroshot text classification module build on top of flair library. It uses `tars-base` model for text classification

This tutorial shows you how to import and use `zs_classifier` with jac code.


1. Import [ZS Classifier](#1-import-zeroshot-classfierzsclassifier-module-in-jac) module in jac
2. ZeroShot [Predictions](#2-zeroshot-predictions)
3. ZeroShot [Embeddings](#3-zeroshot-embeddings)


## **Walk through**

### **1. Import `ZeroShot Classfier(zs_classifier)` module in jac**
1. Open terminal and run jaseci by cmd
    > jsctl -m
2. Load `zs_classifier` module in jac by cmd
    > actions load module jac_nlp.zs_classifier
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
        * `classify`: used to classify text among the classes provided
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

### **3. ZeroShot Embeddings** 
* **Creating  a Jac Walker (`get_embeddings`)**
    1. Create `get_embeddings` walker in the `zs_classifier.jac`
        ```jac
            walker test_get_embedding{
                can zs_classifier.get_embeddings;
                report zs_classifier.get_embeddings(texts="I am so glad you liked it!");
            }
        ```

        **Parameter details**
        * `get_embeddings`: can be used to get embeddings for text from zs model
            * Input:
                * `text` (str or List(str)): it can be string or list of string 
            * Returns: list of embdedding of length 768 size

* **Steps for running `zs_classifier.jac` program**

    1. Build `zs_classifier.jac` by run cmd
        > jac build zs_classifier.jac
    2. Activate sentinal by run cmd
        > sentinel set -snt active:sentinel -mode ir zs_classifier.jir
    3. Calling walker `get_embeddings` with `default parameter`
        > walker run get_embeddings </br>

    **Expected output**
    ```
   [
    0.15722215175628662,
    -0.2446146011352539,
    0.7713489532470703,
    0.20605269074440002,
    ...
    ...
    ...
    ...
    -0.4917687475681305,
    0.17996184527873993,
    -0.39374977350234985,
    0.3616657555103302
    ]
    ```