## FastText Classifier
Stand up fastAPI server locally
```
uvicorn fasttext:app --host 0.0.0.0 --port 80
```
Stand up in a k8s environment
```
kubectl apply -f fasttext.yaml
```
