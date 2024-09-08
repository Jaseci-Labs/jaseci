# **Large Language Models (`llm`)**
> **_NOTE:_**  This module only works with CUDA enabled devices. If you run into any bitsandbytes error, try checking the CUDA version of your device and replace the `libbitsandbytes_cpu.so` with `libbitsandbytes_cuda<version>.so` in `/home/<USER>/anaconda3/envs/llm/lib/python3.10/site-packages/bitsandbytes/` directory.
```bash

Large Language Models (`llm`) is a Jaseci module that allows you to generate text using large language models and also perform parameter efficient transfer learning using your own data.
## **Usecases**
- Generate text using large language models.
- Perform parameter efficient transfer learning using your own data.
- Emulate a chatbot.
- Generate a response to a question.
- Generate a response to a question with a given context.

> Mind is the limit. As long as the mind can envision the fact that you can do something, you can do it, as long as you really believe 100 percent. - Arnold Schwarzenegger

## **Actions**
### **Setup (`setup`)**
The `setup` action allows you to setup the module.

Inputs:
- model_name: string (default: "databricks/dolly-v2-3b"). You can use any model from [HuggingFace LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard).
- lora_dir: string (default: None). This is the directory where the lora files will be stored.
- tokenizer_name: string (default: model_name - will use the tokenizer provided witht the model).
- tokenizer_kwargs: dict (default: {}) - kwargs for the tokenizer. Refer [AutoTokenizer.from_pretrained](https://huggingface.co/docs/transformers/main/en/model_doc/auto#transformers.AutoTokenizer.from_pretrained) for more details.
- model_kwargs: dict (default: {}) - kwargs for the model. Refer [AutoModelForCausalLM.from_pretrained](https://huggingface.co/docs/transformers/main/en/model_doc/auto#transformers.AutoModelForCausalLM.from_pretrained) for more details.

#### **Example**
Running the Setup action while loading the module.
```bash
jaseci> actions load module jac_nlp.llm -ctx '{"model_name": "databricks/dolly-v2-3b", "lora_dir": "dolly", "tokenizer_kwargs": {"max_length": 1024}}'
```
Running the Setup action after loading the module.
```bash
jaseci> actions call dolly.setup -ctx '{"model_name": "databricks/dolly-v2-3b", "lora_dir": "dolly", "tokenizer_kwargs": {"max_length": 1024}}'
```

### **Generate (`generate`)**
The `generate` action allows you to generate text based on the input text you provide.

Inputs:
- prompt: input text, string
- kwargs: input variables, dict (temperature, max_length etc.)

Output
- list of generated text, list of dicts
```json
[
    {
        "generated_text": "generated text 1"
    },
    {
        "generated_text": "generated text 2"
    }
]
```

#### **Example**
Using JSCTL
```bash
jaseci> actions call llm.generate -ctx '{"prompt": "Hello, how are you?"}'
```
Using JAC
```jac
walker test_generate {
    can llm.generate;
    report llm.generate(prompt="Hello, how are you?");
}
```
## **Training (`train`)**
The `train` action allows you to perform parameter efficient transfer learning (LoRA) using your own data.

Inputs:
- data_file: string (Required). This is the path to the JSON file. the file should follow the following format.
```json
[
    {
        "instruction": "Give three tips for staying healthy.",
        "input": "",
        "output": "1.Eat a balanced diet and make sure to include plenty of fruits and vegetables. \n2. Exercise regularly to keep your body active and strong. \n3. Get enough sleep and maintain a consistent sleep schedule."
    },
    {
        "instruction": "Convert the following sentence into the present continuous tense",
        "input": "He reads books",
        "output": "He is reading books."
    }
]
```
You can use this [GUI](https://github.com/gururise/AlpacaDataCleaned/tree/main/gui) to generate your own data.
- output_dir: string (Required). This is the directory where the trained model will be stored.
- training_params: dict (default: DEFAULT_TRAINING_PARAMS). This is the some of the training parameters for the model and the LoRA configuration.
- lora_config_kwargs: dict (default: {}). This is the kwargs for the LoRA configuration. Refer [peft.LoraConfig](https://huggingface.co/docs/peft/main/en/package_reference/tuners#peft.LoraConfig) for more details.
- training_args_kwargs: dict (default: {}). This is the kwargs for the training arguments. Refer [transformers.Trainer](https://huggingface.co/docs/transformers/v4.29.1/en/main_classes/trainer#transformers.Trainer) for more details.

#### **Example**
Using JSCTL
```bash
jascei> actions call llm.train -ctx '{"data_file": "data.json", "output_dir": "output"'
```
## **References**
- [HuggingFace LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)
- PEFT: Parameter-Efficient Fine-Tuning for Transformers via Probabilistic Early Exiting, [arXiv:2106.01345](https://arxiv.org/abs/2106.01345)
- LoRA: Low-Rank Adaptation of Large Language Models, [arXiv:2106.09680](https://arxiv.org/abs/2106.09680)