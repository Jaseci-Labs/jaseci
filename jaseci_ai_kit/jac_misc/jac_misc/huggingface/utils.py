API_ENDPOINTS = {
    "feature_extraction": {
        "default": {
            "API_URL": "https://api-inference.huggingface.co/models/facebook/bart-large",
            "API_TYPE": "input",
        },
        "unsup-simcse-roberta-base": {
            "API_URL": "https://api-inference.huggingface.co/models/princeton-nlp/unsup-simcse-roberta-base",
            "API_TYPE": "input",
        },
        "conv-bert-base": {
            "API_URL": "https://api-inference.huggingface.co/models/YituTech/conv-bert-base",
            "API_TYPE": "input",
        },
        "codebert-base": {
            "API_URL": "https://api-inference.huggingface.co/models/microsoft/codebert-base",
            "API_TYPE": "input",
        },
        "specter": {
            "API_URL": "https://api-inference.huggingface.co/models/allenai/specter2",
            "API_TYPE": "input",
        },
    },
    "text-to-image": {
        "default": {
            "API_URL": "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
            "API_TYPE": "input",
        },
        "stable-diffusion-v1-4": {
            "API_URL": "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4",
            "API_TYPE": "input",
        },
        "stable-diffusion-v2-1": {
            "API_URL": "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1",
            "API_TYPE": "input",
        },
    },
    "image-classification": {
        "default": {
            "API_URL": "https://api-inference.huggingface.co/models/microsoft/resnet-50",
            "API_TYPE": "file",
        },
        "convnext-large-224": {
            "API_URL": "https://api-inference.huggingface.co/models/facebook/convnext-large-224",
            "API_TYPE": "file",
        },
        "resnet-18": {
            "API_URL": "https://api-inference.huggingface.co/models/microsoft/resnet-18",
            "API_TYPE": "file",
        },
        "vit-base-patch16-224": {
            "API_URL": "https://api-inference.huggingface.co/models/google/vit-base-patch16-224",
            "API_TYPE": "file",
        },
    },
    "object-detection": {
        "default": {
            "API_URL": "https://api-inference.huggingface.co/models/hustvl/yolos-tiny",
            "API_TYPE": "file",
        },
        "detr-resnet-50": {
            "API_URL": "https://api-inference.huggingface.co/models/facebook/detr-resnet-50",
            "API_TYPE": "file",
        },
        "detr-resnet-101": {
            "API_URL": "https://api-inference.huggingface.co/models/facebook/detr-resnet-101",
            "API_TYPE": "file",
        },
        "yolos-small": {
            "API_URL": "https://api-inference.huggingface.co/models/hustvl/yolos-small",
            "API_TYPE": "file",
        },
    },
    "image-segementation": {
        "default": {
            "API_URL": "https://api-inference.huggingface.co/models/nvidia/segformer-b0-finetuned-ade-512-512",
            "API_TYPE": "file",
        },
        "upernet-convnext-small": {
            "API_URL": "https://api-inference.huggingface.co/models/openmmlab/upernet-convnext-small",
            "API_TYPE": "file",
        },
        "detr-resnet-50-panoptic": {
            "API_URL": "https://api-inference.huggingface.co/models/facebook/detr-resnet-50-panoptic",
            "API_TYPE": "file",
        },
        "segformer-b5-finetuned-ade-640-640": {
            "API_URL": "https://api-inference.huggingface.co/models/nvidia/segformer-b5-finetuned-ade-640-640",
            "API_TYPE": "file",
        },
    },
    "sentiment-analysis": {
        "default": {
            "API_URL": "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english",
            "API_TYPE": "input",
        },
        "twitter-roberta-base-sentiment": {
            "API_URL": "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment",
            "API_TYPE": "input",
        },
        "twitter-xlm-roberta-base-sentiment": {
            "API_URL": "https://api-inference.huggingface.co/models/cardiffnlp/twitter-xlm-roberta-base-sentiment",
            "API_TYPE": "input",
        },
    },
    "named-entity-recognition": {
        "default": {
            "API_URL": "https://api-inference.huggingface.co/models/Davlan/distilbert-base-multilingual-cased-ner-hrl",
            "API_TYPE": "input",
        },
        "bert-base-NER": {
            "API_URL": "https://api-inference.huggingface.co/models/dslim/bert-base-NER",
            "API_TYPE": "input",
        },
        "ner-english-fast": {
            "API_URL": "https://api-inference.huggingface.co/models/flair/ner-english-fast",
            "API_TYPE": "input",
        },
    },
    "table-question-answering": {},
    "question-answering": {},
    "zero-shot-classification": {},
    "translation": {},
    "summarization": {},
    "conversation": {},
    "text-generation": {},
    "text2text-generation": {},
    "fill_mask": {
        "bert-base-uncased": {
            "API_URL": "https://api-inference.huggingface.co/models/bert-base-uncased",
            "API_TYPE": "input",
        }
    },
    "sentence-similarity": {},
    "text-to-speech": {},
    "automatic-speech-recognition": {},
    "audio-to-audio": {},
    "audio-classification": {},
    "voice-activity-detection": {},
    "tabular-classification": {},
    "tabular-regression": {},
    "reinforcement-learning": {},
    "robotics": {},
}
