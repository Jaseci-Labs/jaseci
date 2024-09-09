from jaseci.jsorc.live_actions import jaseci_action
from jaseci.utils.utils import logger
import torch
from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import prepare_model_for_int8_training, LoraConfig, get_peft_model, PeftModel
from datasets import load_dataset
import transformers
import os

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


@jaseci_action(act_group=["llm"], allow_remote=True)
def setup(
    model_name: str = "databricks/dolly-v2-3b",
    lora_dir: str = None,
    tokenizer_name: str = None,
    **kwargs,
):
    global pipeline, model, tokenizer

    tokenizer_kwargs = kwargs.get("tokenizer_kwargs", {})
    tokenizer = AutoTokenizer.from_pretrained(
        tokenizer_name if tokenizer_name else model_name, **tokenizer_kwargs
    )
    model_kwargs = kwargs.get("model_kwargs", {})
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16,
        load_in_8bit=True,
        **model_kwargs,
    )
    logger.info("Model loaded")
    if lora_dir:
        model = PeftModel.from_pretrained(
            model, lora_dir, device_map="auto", torch_dtype=torch.float16
        )
        logger.info("Lora loaded")

    pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
    logger.info("Pipeline created")


@jaseci_action(act_group=["llm"], allow_remote=True)
def generate(prompt: str, **kwargs):
    return pipeline(prompt, **kwargs)


@jaseci_action(act_group=["llm"], allow_remote=True)
def train(
    data_file: str,
    output_dir: str,
    training_params=DEFAULT_TRAINING_PARAMS,
    resume_from_checkpoint=False,
    **kwargs,
):
    global model, tokenizer
    os.makedirs(
        output_dir, exist_ok=True
    )  # create output directory if it doesn't exist

    BATCH_SIZE = training_params.get(
        "BATCH_SIZE", DEFAULT_TRAINING_PARAMS["BATCH_SIZE"]
    )
    MICRO_BATCH_SIZE = training_params.get(
        "MICRO_BATCH_SIZE", DEFAULT_TRAINING_PARAMS["MICRO_BATCH_SIZE"]
    )
    EPOCHS = training_params.get("EPOCHS", DEFAULT_TRAINING_PARAMS["EPOCHS"])
    LEARNING_RATE = training_params.get(
        "LEARNING_RATE", DEFAULT_TRAINING_PARAMS["LEARNING_RATE"]
    )
    CUTOFF_LEN = training_params.get(
        "CUTOFF_LEN", DEFAULT_TRAINING_PARAMS["CUTOFF_LEN"]
    )
    LORA_R = training_params.get("LORA_R", DEFAULT_TRAINING_PARAMS["LORA_R"])
    LORA_ALPHA = training_params.get(
        "LORA_ALPHA", DEFAULT_TRAINING_PARAMS["LORA_ALPHA"]
    )
    LORA_DROPOUT = training_params.get(
        "LORA_DROPOUT", DEFAULT_TRAINING_PARAMS["LORA_DROPOUT"]
    )
    GRADIENT_ACCUMULATION_STEPS = BATCH_SIZE // MICRO_BATCH_SIZE

    # Preparing the model for int8 training
    model = prepare_model_for_int8_training(model, use_gradient_checkpointing=True)
    config = LoraConfig(
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        lora_dropout=LORA_DROPOUT,
        bias="none",
        task_type="CAUSAL_LM",
        **kwargs.get("lora_config_kwargs", {}),
    )
    model = get_peft_model(model, config)
    tokenizer.pad_token_id = 0

    # Preparing the dataset
    data = load_dataset("json", data_files=data_file)
    data = data.shuffle().map(
        lambda data_point: tokenizer(
            generate_prompt(data_point),
            truncation=True,
            max_length=CUTOFF_LEN,
            padding="max_length",
        )
    )

    trainer = transformers.Trainer(
        model=model,
        train_dataset=data["train"],
        args=transformers.TrainingArguments(
            per_device_train_batch_size=MICRO_BATCH_SIZE,
            gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
            warmup_steps=20,
            num_train_epochs=EPOCHS,
            learning_rate=LEARNING_RATE,
            fp16=True,
            logging_steps=1,
            output_dir=output_dir,
            save_total_limit=3,
            **kwargs.get("training_args_kwargs", {}),
        ),
        data_collator=transformers.DataCollatorForLanguageModeling(
            tokenizer, mlm=False
        ),
    )
    model.config.use_cache = False

    trainer.train(resume_from_checkpoint=resume_from_checkpoint)

    # Saving the model
    os.makedirs(os.path.join(output_dir, "final"), exist_ok=True)
    model.save_pretrained(os.path.join(output_dir, "final"))


@jaseci_action(act_group=["llm"], allow_remote=True)
def generate_prompt(data_point):
    # taken from https://github.com/tloen/alpaca-lora
    if data_point["input"]:
        return f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

        ### Instruction:
        {data_point["instruction"]}

        ### Input:
        {data_point["input"]}

        ### Response:
        {data_point["output"]}"""
    else:
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

        ### Instruction:
        {data_point["instruction"]}

        ### Response:
        {data_point["output"]}"""


@jaseci_action(act_group=["llm"], allow_remote=True)
def run_dataset_builder():
    import streamlit.web.bootstrap

    streamlit.web.bootstrap.run(
        os.path.join(os.path.dirname(__file__), "dataset_builder.py"), "", [], []
    )
