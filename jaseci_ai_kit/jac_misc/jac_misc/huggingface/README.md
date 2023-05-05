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

## Models
The following tasks are supported by the `query` action. The required parameters for each task are listed in the table below. The default model for each task is also listed in the table. You can find the available models for each task [here](https://huggingface.co/models).

| Task | Model | Required Parameters | example input |
| --- | --- | --- | --- |
| feature-extraction | `bart-large (default)` | `inputs` | |
| feature-extraction | `unsup-simcse-roberta-base` | `inputs` | |