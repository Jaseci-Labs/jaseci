## **Steps for running mlflow experirment and mlflow server with sqlite db**

**Enter inside module entity_extraction_type_2 and open terminal and execute below commands,**

**NOTE** : `first execute mlflow server(else will get error)`

## 1. Run mlflow server by command:

```
mlflow server --backend-store-uri sqlite:///mlrunsdb15.db --default-artifact-root file:/mlruns -h 0.0.0.0 -p 5000
```

## 2. Run Experiment by command:
```
python entity_extraction.py
```
## 3. Run url in brouser for executing api
```
http://127.0.0.1:8000/
```
1. pass data and execute model training 

## 4. For view logging in brouser by executing below url
```
http://127.0.0.1:5000/
```
