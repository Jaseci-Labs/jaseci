API_ENDPOINTS = {
	"feature_extraction": {
        "default": {
			"API_URL": "https://api-inference.huggingface.co/models/facebook/bart-large",
			"PARAMETERS": ["inputs"]
        },
        "unsup-simcse-roberta-base": {
            "API_URL": "https://api-inference.huggingface.co/models/princeton-nlp/unsup-simcse-roberta-base",
	        "PARAMETERS": ["inputs"]
        },
        "conv-bert-base": {
            "API_URL": "https://api-inference.huggingface.co/models/YituTech/conv-bert-base",
	        "PARAMETERS": ["inputs"]
        },
	    "codebert-base": {
            "API_URL": "https://api-inference.huggingface.co/models/microsoft/codebert-base",
            "PARAMETERS": ["inputs"]
        },
	    "specter" : {
		    "API_URL": "https://api-inference.huggingface.co/models/allenai/specter2",
		    "PARAMETERS": ["inputs"]
        }
    },
	"text-to-image": {},
	"image-to-text": {},
	"text-to-video":{},
	"visual-question-answering": {},
	"document-question-answering": {},
	"graph-machinelearning": {},
	"depth-estimation": {},
	"image-classification": {},
	"object-detection": {},
	"image-segementation": {},
	"image-to-image": {},
	"unconditional-image-generation": {},
	"video-classification": {},
	"zero-shot-image-classification": {},
	"text-classification": {},
	"token-classification": {},
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
		    "PARAMETERS": ["inputs"]
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
    "robotics": {}
}