from jaseci.jsorc.live_actions import jaseci_action
from jaseci.jsorc.remote_actions import launch_server
from fastapi import HTTPException

from .action_utils import (
    create_series,
    train_test_split,
    normalize,
    transformer_model,
    define_covariates,
    train_model,
    eval,
)


@jaseci_action(act_group=["forecast"], allow_remote=True)
def preprocess(time: list, variables: dict):
    try:
        global timeseries
        timeseries = create_series(time, variables)
        return "Time series object created successfully!"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["forecast"], allow_remote=True)
def split(cuttoff: str, scale: bool):
    try:
        global train
        global validation
        train, validation = train_test_split(timeseries, cuttoff, scale)
        return "Data splitted in to train and validation successfully!"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["forecast"], allow_remote=True)
def scale():
    try:
        global timeseries
        timeseries = normalize(timeseries)
        return "Timeseries data scaled successfully!"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["forecast"], allow_remote=True)
def create_model(model_name: str, parameters: dict):
    if model_name == "transformer":
        # add error handling in this, check if dictionary keys,values exists
        global model
        model = transformer_model(
            input_chunk=parameters["input_chunk"],
            output_chunk=parameters["output_chunk"],
            hidden_size=parameters["hidden_size"],
            quantiles=parameters["quantiles"],
        )
        return "Model created successfully!"
    else:
        return "The model creation failed!, check the model name"


@jaseci_action(act_group=["forecast"], allow_remote=True)
def train(covariate1, covariate2):
    covariates = define_covariates(timeseries, covariate1, covariate2)
    global model
    model = train_model(model, train, covariates)


@jaseci_action(act_group=["forecast"], allow_remote=True)
def evaluate(n: int, num_samples: int = 2):
    try:
        return eval(model, n, validation, num_samples=num_samples)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["forecast"], allow_remote=True)
def predict(n: int, num_samples: int = 2):
    try:
        pred_series = model.predict(n=n, num_samples=num_samples)
        return pred_series.values().tolist()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
