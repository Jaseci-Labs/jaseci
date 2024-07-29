# Finetuning Scripts
The default `config.yaml` provides an example of how to finetune a SmolLM model for the Map Generation Task. Depending on your specific task, you can modify the `config.yaml` file to finetune the model accordingly. Follow the steps below to finetune the model:

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. If you plan to push the model to the Hugging Face Model Hub, follow these steps and make sure to save the key in the git repository to avoid losing it:
```bash
huggingface-cli login
```

3. To finetune the model, run the following command:
```bash
python train.py --config config.yaml --push_to_hf
```

4. To push the model to the Hugging Face Model Hub, use the following command:
```bash
python merge_n_push.py --config config.yaml --checkpoint 500
```
If you don't want to push the model to the Hugging Face Model Hub, you can remove the `--push_to_hf` flag.

5. Test the trained using the `test.ipynb` notebook. You can also run it in Google Colab by clicking the badge below:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://github.com/Jaseci-Labs/mtllm/blob/main/support/finetune_llm/test.ipynb)
```bash

6. To evaluate the model, run the following command:
```bash
python evaluate.py --config config.yaml --checkpoint 500 --eval_data chandralegend/mtllm_eval
```
Make sure to replace `checkpoint` with the desired checkpoint number and `eval_data` with the dataset you want to evaluate on. The dataset should be available in the Hugging Face Dataset Hub.
