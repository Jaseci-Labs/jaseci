# Finetuning Scripts

The default `config.yaml` provides an example of how we finetuned a SmolLM model for Map Generation Task. according to
your task, you can change the `config.yaml` file to finetune the model for your task. follow the steps below to finetune

Install the requirements:
```bash
pip install -r requirements.txt
```

If you are thinking of pushing the model to the huggingface model hub, follow the steps below, remmeber to save the key
to the git repository, so that the key is not lost.
```bash
huggingface-cli login
```

To finetune the model, run the following command:
```bash
python train.py --config config.yaml --push_to_hf
```

Use the `--push_to_hf` flag to push the model to the huggingface model hub. If you don't want to push the model to the
huggingface model hub, you can remove the flag.

To evaluate the model, run the following command:
```bash
python evaluate.py --config config.yaml --checkpoint 500 --eval_data chandralegend/mtllm_eval
```
change the `checkpoint` to the checkpoint you want to evaluate.
change the `eval_data` to the dataset you want to evaluate on. it should be a dataset in the huggingface dataset hub.