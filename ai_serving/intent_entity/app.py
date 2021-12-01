from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification

#zero-Shot_model
zs_model_name="joeddav/bart-large-mnli-yahoo-answers"
zs_pipeline = pipeline("zero-shot-classification", model=zs_model_name)
print("Label Classification Model Loaded\n")
#NER-Model
ner_model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
tokenizer = AutoTokenizer.from_pretrained(ner_model_name)
model = AutoModelForTokenClassification.from_pretrained(ner_model_name)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)
print("NER Model Loaded\n")

def intentClassification(text):
    candidate_labels = ["News", "Travel", "Weather", "Greet"]
    zs_results = zs_pipeline(text, candidate_labels, multi_label=True)
    print("Label Classification Score :\n")
    print(f'Text : {zs_results["sequence"]} \n\t\tIntents\t\t\t\t\t\tScores\n{zs_results["labels"]} : {zs_results["scores"]}')

def entityDetection(text):
    ner_results = ner_pipeline(text)
    print("\nEntity Classification Score :\n")
    print(ner_results)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Need text for NLP')
    parser.add_argument('--text', metavar='text', required=True,
                        help='input to the model')
    args = parser.parse_args()
    intentClassification(text=args.text)
    entityDetection(text=args.text)