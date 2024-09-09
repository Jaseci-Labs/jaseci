# **HuggingFace API (`hf`)**

Module `hf` provides the jac users to easily use the HuggingFace API. You can use the actions to generate text, transcribe audio, translate audio, generate images, and more.

## **1. Setup**
You have to set the HuggingFace API key before using the module. You can get the API key from [here](https://huggingface.co/settings/tokens). You can set the API key using the `setup` action or by setting the environment variable `HUGGINGFACE_API_KEY`.

### Setting the Environment Variable
```bash
export HUGGINGFACE_API_KEY=<your-api-key>
```
Then you can load the module as usual as follows.
```bash
jaseci> actions load module jac_misc.huggingface
```

### Using the `setup` Action
If you have already loaded the module, you can use the `setup` action to set the API key.
```bash
jaseci> actions call hf.setup -ctx '{"api_key":"<your-api-key>"}'
```
Otherwise you can load the module and set the API key in a single step as follows.
```bash
jaseci> action load module jac_misc.huggingface -ctx '{"api_key":"<your-api-key>"}'
```

## **2. Usage**
### Using the `query` Action
You can use the `query` action to query the HuggingFace API. The `query` action takes the following parameters.

#### Parameters:

- `task`: str, optional (default=`None`)
    The task to query the API for. The available tasks are listed [here](#Models).
- `model`: str, optional (default=`default`)
    The name of the model to use for the task. If not provided, the default model for the task will be used. Check [here](#Models) for the default models for each task and the available models for each task.
- `api_url`: str, optional (default=`None`)
    The URL of the HuggingFace API or Custom HF Inference Endpoint.
- `api_type`: str, optional (default=`None`)
    The type of the HuggingFace API. The available types are `inputs` and `file`.
- `other parameters`: required for each task
    The parameters required for each task are listed [here](#example).

#### Returns:
The `query` action returns the response from the HuggingFace API as a JSON output.


#### Example:
```jac
walker get_embedding {
    can hf.query;
    report hf.query(task="feature-extraction", model="conv-bert-base", inputs="Hello World!");
}
```
Using your custom HF Inference Endpoint:
```jac
walker get_embedding {
    can hf.query;
    report hf.query(api_url="https://my-custom-hf-endpoint.com", api_type="inputs", inputs="Hello World!" );
}
```

## Models
The following tasks are supported by the `query` action. The required parameters for each task are listed in the table below. The default model for each task is also listed in the table. You can find the available models for each task [here](https://huggingface.co/models).

| Task                 | Model                | Required Parameters | Example code                                                                                          |
| -------------------- | -------------------- | ------------------- | ----------------------------------------------------------------------------------------------------- |
| feature-extraction   | bart-large (default) | `inputs`            | `hf.query(task="feature-extraction", inputs="Today is a sunny day and I'll get some ice cream.")`     |
|                      | `unsup-simcse-roberta-base` | `inputs` | `hf.query(task="feature-extraction", model="unsup-simcse-roberta-base", inputs="Today is a sunny day and I'll get some ice cream.")`|
|                      | `conv-bert-base` | `inputs` | `hf.query(task="feature-extraction", model="conv-bert-base", inputs="Today is a sunny day and I'll get some ice cream.")`|
|                      | `codebert-base` | `inputs` | `hf.query(task="feature-extraction", model="codebert-base", inputs="Today is a sunny day and I'll get some ice cream.")`|
|                      | `specter` | `inputs` | `hf.query(task="feature-extraction", model="specter", inputs="Today is a sunny day and I'll get some ice cream.")`|
| text-to-image        | stable-diffusion-v1-5 (default) | `inputs` | `hf.query(task="text-to-image", inputs="Today is a sunny day and I'll get some ice cream.")`         |
|                      | `stable-diffusion-v1-4` | `inputs` | `hf.query(task="text-to-image", model="stable-diffusion-v1-4", inputs="Today is a sunny day and I'll get some ice cream.")`|
|                      | `stable-diffusion-v2-1` | `inputs` | `hf.query(task="text-to-image", model="stable-diffusion-v2-1", inputs="Today is a sunny day and I'll get some ice cream.")`|
| image-classification | resnet-50 (default) | `file` | `hf.query(task="image-classification", file="path/to/image.jpg")`                                     |
|                      | `resnet-18`         | `file`              | `hf.query(task="image-classification", model="resnet-18", file="path/to/image.jpg")`                 |
|                      | `convnext-large-224`| `file`              | `hf.query(task="image-classification", model="convnext-large-224", file="path/to/image.jpg")`        |
|                      | `vit-base-patch16-224`| `file`            | `hf.query(task="image-classification", model="vit-base-patch16-224", file="path/to/image.jpg")`      |
| object-detection     | yolos-tiny (default)     | `file`              | `hf.query(task="object-detection", file="path/to/image.jpg")`                                         |
|                      | `detr-resnet-50`   | `file`              | `hf.query(task="object-detection", model="detr-resnet-50", file="path/to/image.jpg")`                |
|                      | `detr-resnet-101`   | `file`              | `hf.query(task="object-detection", model="detr-resnet-101", file="path/to/image.jpg")`                |
|                      | `yolos-small`      | `file`              | `hf.query(task="object-detection", model="yolos-small", file="path/to/image.jpg")`                   |
| image-segmentation   | segformer-b0-finetuned-ade-512-512 (default) | `file`              | `hf.query(task="image-segmentation", file="path/to/image.jpg")`                                       |
|                      | `upernet-convnext-small` | `file`              | `hf.query(task="image-segmentation", model="upernet-convnext-small", file="path/to/image.jpg")`      |
|                      | `detr-resnet-50-panoptic` | `file`              | `hf.query(task="image-segmentation", model="detr-resnet-50-panoptic", file="path/to/image.jpg")`      |
|                      | `segformer-b5-finetuned-ade-640-640` | `file`              | `hf.query(task="image-segmentation", model="segformer-b5-finetuned-ade-640-640", file="path/to/image.jpg")`      |
| sentiment-analysis   | distilbert-base-uncased-finetuned-sst-2-english (default) | `inputs` | `hf.query(task="sentiment-analysis", inputs="Today is a sunny day and I'll get some ice cream.")`   |
|                      | `twitter-roberta-base-sentiment` | `inputs` | `hf.query(task="sentiment-analysis", model="twitter-roberta-base-sentiment", inputs="Today is a sunny day and I'll get some ice cream.")`   |
|                      | `twitter-xlm-roberta-base-sentiment` | `inputs` | `hf.query(task="sentiment-analysis", model="twitter-xlm-roberta-base-sentiment", inputs="Today is a sunny day and I'll get some ice cream.")`   |
| named-entity-recognition   | distilbert-base-multilingual-cased-ner-hrl (default) | `inputs`            | `hf.query(task="named-entity-recognition", inputs="Today is a sunny day and I'll get some ice cream.")`   |
|                      | `bert-base-NER`     | `inputs`            | `hf.query(task="named-entity-recognition", model="bert-base-NER", inputs="Today is a sunny day and I'll get some ice cream.")`   |
|                      | `ner-english-fast`  | `inputs`            | `hf.query(task="named-entity-recognition", model="ner-english-fast", inputs="Today is a sunny day and I'll get some ice cream.")`   |
| fill-mask           | bert-base-uncased (default) | `inputs`            | `hf.query(task="fill-mask", inputs="Today is a sunny day and I'll get some ice cream.")`   |