# Jaseci Kit Module + MLFlow Integration Guide

## Implement MLFlow logging function

### 1.Set tracking URI
This connects to a tracking URI. You can also set the MLFLOW\_TRACKING\_URI environment variable to have MLflow find a URI from there. In both cases, the URI can either be a HTTP/HTTPS URI for a remote server, a database connection string, or a local path to log data to a directory. The URI defaults to mlruns.

```
tracking\_uri = "sqlite:///mlrunsdb15.db"

## url for connecting database to storing parameter and metrics data in mlflow

mlflow.set\_tracking\_uri(tracking\_uri)
```

### 2. Getting or creating experiment id
```py
experiment_id = mlflow.get_experiment_by_name("TFM_NER")
if experiment_id is None:
    experiment_id = mlflow.create_experiment("TFM_NER")
    experiment_id = mlflow.get_experiment_by_name("TFM_NER").experiment_id
else:
    experiment_id = experiment_id.experiment_id
```
### 3. Writing metrics data to local or in DB by adding MLFlow log metric
Logs a single key-value metric. The value must always be a number. MLflow remembers the history of values for each metric.

#### Storing training metrics by below code, on every epochs
```py
mlflow.log_metric("Train Epoch Loss", epoch_loss, step=nb_tr_steps)
mlflow.log_metric("Train Epoch Accuracy", tr_acc, step=nb_tr_steps)
```
#### Storing validation metrics by below code, on every epochs
```py
mlflow.log_metric("Val epoch loss", ev_epoch_loss, step=nb_ev_steps)
mlflow.log_metric("Val epoch accuracy", ev_acc, step=nb_ev_steps)
```

#### Storing Testing metrics by below code, on every epochs
```
mlflow.log_metric("Test f1_macro", f_macro)
mlflow.log_metric("Test accuracy", tst_acc)
```

### 4. Start Training with MLFlow
Start a new MLflow run, setting it as the active run under which metrics and parameters will be logged. The return value can be used as a context manager within a with block
```py
with mlflow.start_run(
    run_name="ner_type2",
    experiment_id=experiment_id,
    nested=True,
    description="Hugging face transformer based ner model",
    ):
    # Training code follows
```

* **Run_name** is name of running experiment run **.**
* **Experiment Id**** :** unique id for experiment
* **Nested** : If it's **true** then we can re-run training again other than need to stop current run.

### 5. Training parameter:
For storing training parameter need to add
```py
mlflow.log_params(training_parameters)
```
* **training_parameters**: it's dictionary of training parameter.

### 6. `save_custom_model:` saving the best model data in temp directory

### 7. Logging the model artifact
This is the model data file (additional file that required with Pytorch token classification model).
```py
mlflow.log_artifacts(
    f"{model_save_path}/curr_checkpoint/{model_name}",
    artifact_path="pytorch_model/model",
)
```
MLFlow logging the model data in mlrun directory. Passing the model temp data path and artifact storing path in mlrun directory.

### 8. Logging model data and register model
Logging model data in mlrun directory and registering trained model.
```py
mlflow.pytorch.log_model(
    model,
    artifact_path="pytorch_model", registered_model_name=mod_name
)
```

### 9. Getting model versions
Passing the parameter model run name and get all registered version of model.
```py
client.search_model_versions(f"name='{name}'")
```

### 10. Create model transition
Passing parameter model name and version and stage to transition model on that stage (i.e. "Production" or "Staging")
```py
transition(model_name=mod_name, version=version, stage="Staging")
```

# Running experiment and executing APIs

### 1. Execute the mlflow server with sqlite Database
```bash
mlflow server --backend-store-uri sqlite:///mlrunsdb15.db --default-artifact-root file:/mlruns -h 0.0.0.0 -p 5000
```
### 2. And now execute the module(tfm_ner type2)
```bash
python entity_extraction.py
```

### 3. Go to MLFlow web UI URL
```
http://127.0.0.1:8000/
```

### 4. **For view logging in browser by executing below url**
```
http://127.0.0.1:5000/

```
## Description of API's,

1. **extract\_entity** : Api for predicting new data on staging model. Pass the parameter text and will predict entity from text with staging model

2. **prod\_extract\_entities :** Pass the parameter ` text` will predict entity with production model

3. **train:** pass the below parameter and execute training.
```json
{
    "mode": "default",
    "epochs": 10,
    "train_data": [],
    "val_data": [],
    "test_data": []
}
```

After executing training, model will be trained on the new datasets and parameter will stored in database and artifact will stored on local storage and model will register as new version on staging environment.

Will show on MLflow dashboard open default url [http://127.0.0.1:5000/](http://127.0.0.1:5000/) and open Experiment `TFM_NER`.

* Inside experiment will show all parameter data and metrics data and also show artifact data.
* Inside parameter dropdown will show all parameter data.
* Inside metrics dropdown will stored metrics data.
* Graph on metrics data.
* Artifact dropdown will store saved model data and its required file.
* Open model tab will show details of selected model and show active stages of model.
* Open the link model name will show on the all available model versions

4. **load_model:** this API will load the new hugging face token classification model in staging. Then we perform training on this. Here we need to pass the parameter "model name"

5. **prod_load_model:** this will loading the model in production environment. Its take three parameter

```json
{
    "prod_model_path": "registered_model_path",
    "prod_model_name": "tfm_ner_type2",
    "prod_version": 1
}
```
* prod_model_path : its path of registered model.
* prod_model_name : name of model
* prod_version : version of model

6. **get_model_version:** It take parameter as "model\_name" and will return all model version with details.

7. **save_model:** will take parameter "model\_path" for saving the current running model from staging.

8. **get_train_config** : will not take any argument and return all training configuration

9. **set_train_config:** will take "training\_parameters" dictionary of parameters and stored as default training config file.

10. **get_model_config** : will not take any argument and return all default model parameters.

11. **set_model_config** : will take arguments "model\_parameters" and set as default model configuration.