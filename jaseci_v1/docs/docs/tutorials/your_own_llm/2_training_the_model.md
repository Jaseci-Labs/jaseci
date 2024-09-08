---
sidebar_position: 2
title: Training the model
description: How to train your own Instruction model using the dataset you created
---

# Training the model

we will be fine-tuning Dolly v2, a pre-existing language model, using the Alpaca Cleaned Dataset and the LoRA technique. This step is crucial for adapting the language model to our specific domain and task.

To initiate the training process, we will utilize the Jaseci platform and execute the following command:

```bash
# Action module need to be loaded if not already loaded (check it using actions list)
jaseci> actions load module jac_nlp.llm
jascei> actions call llm.train -ctx '{"data_file": "dataset.json", "output_dir": "output"}'
```

The `data_file` parameter is the path to the JSON file. In our case we will use the [Alpaca Cleaned Dataset](https://github.com/gururise/AlpacaDataCleaned) (Clone the Repository and used the `alpaca_data_cleaned.json`). The `output_dir` parameter is the directory where the model will be saved. The model checkpoints will be saved in the `output_dir` directory. and after the training is complete, the LoRA weights will be saved in the `output_dir/final` directory.

If you want to train with your own dataset, you can follow the previous steps to create your own dataset and use it to train the model.

## Training Parameters

Using the above given command will use the default training parameters. You can also specify your own training parameters. The following are the training parameters that you can specify:

- training_params: dict (default: DEFAULT_TRAINING_PARAMS). This is the some of the training parameters for the model and the LoRA configuration.
```json
DEFAULT_TRAINING_PARAMS = {
    "MICRO_BATCH_SIZE": 4,
    "BATCH_SIZE": 128,
    "EPOCHS": 2,
    "LEARNING_RATE": 2e-5,
    "CUTOFF_LEN": 256,
    "LORA_R": 4,
    "LORA_ALPHA": 16,
    "LORA_DROPOUT": 0.05,
}
```
- lora_config_kwargs: dict (default: {}). This is the kwargs for the LoRA configuration. Refer [peft.LoraConfig](https://huggingface.co/docs/peft/main/en/package_reference/tuners#peft.LoraConfig) for more details.
- training_args_kwargs: dict (default: {}). This is the kwargs for the training arguments. Refer [transformers.Trainer](https://huggingface.co/docs/transformers/v4.29.1/en/main_classes/trainer#transformers.Trainer) for more details.

Based on your setup, feel free to change the training parameters. For example, if you have a 3090 GPU, you can decrease the `BATCH_SIZE` to Micro Batch size to 2. Want it to be more accurate? Increase the `EPOCHS` to 3 or 4. You can also change the `LEARNING_RATE` to 3e-5 or 5e-5 etc.

---

After the training is complete, you will have the following files in the `output_dir/final` directory:
 - adapter_config.json (LoRA configuration)
 - adapter_model.bin (LoRA weights)

If you want already finetuned lora weights, you can download the [Dolly Alpaca LoRA Weights](https://huggingface.co/samwit/dolly-lora/tree/main) and use it for the next step.