import pandas as pd
import numpy as np

from darts.dataprocessing.transformers import Scaler
from darts import TimeSeries
from darts.utils.timeseries_generation import datetime_attribute_timeseries
from darts.metrics import mape
from darts.models import TFTModel
from darts.utils.likelihood_models import QuantileRegression


def create_series(time: list, variables: dict):
    """
    Create time series object from the data.
    """
    dataframe = pd.DataFrame.from_dict(variables)
    dataframe["time"] = time
    dataframe["time"] = dataframe["time"].apply(lambda x: pd.to_datetime(x))
    dataframe.set_index("time", inplace=True)
    series = TimeSeries.from_times_and_values(times=dataframe.index, values=dataframe)
    series = series.astype(np.float32)
    return series


def train_test_split(series, cuttoff, scale=True):
    """
    Split data as training and validation set
    """
    training_cutoff = pd.Timestamp(cuttoff)
    train, val = series.split_after(training_cutoff)
    if scale:
        transformer = Scaler()
        train_transformed = transformer.fit_transform(train)
        val_transformed = transformer.transform(val)
        return train_transformed, val_transformed
    else:
        return train, val


def define_covariates(series, attribute1="year", attribute2="month"):
    """
    Create year and month covariate series.
    """
    covariates = datetime_attribute_timeseries(
        series, attribute=attribute1, one_hot=False
    )
    covariates = covariates.stack(
        datetime_attribute_timeseries(series, attribute=attribute2, one_hot=False)
    )
    covariates = covariates.astype(np.float32)

    return covariates


def normalize(series):
    """ """
    transformer = Scaler()
    scaled_series = transformer.fit_transform(series)
    return scaled_series


def transformer_model(
    input_chunk,
    output_chunk,
    hidden_size,
    quantiles,
    lstm_layers=1,
    attention_heads=4,
    dropout=0.1,
    batch_size=16,
    n_epochs=300,
    random_state=42,
):
    """
    Creating the transformer model
    """
    model = TFTModel(
        input_chunk_length=input_chunk,
        output_chunk_length=output_chunk,
        hidden_size=hidden_size,
        lstm_layers=lstm_layers,
        num_attention_heads=attention_heads,
        dropout=dropout,
        batch_size=batch_size,
        n_epochs=n_epochs,
        add_relative_index=False,
        add_encoders=None,
        likelihood=QuantileRegression(quantiles=quantiles),
        # loss_fn=MSELoss(),
        random_state=random_state,
    )

    return model


# model training
def train_model(model, train_data, covariates):
    """
    Training the model
    """
    train_model = model.fit(train_data, future_covariates=covariates, verbose=True)
    return train_model


# Model evaluation
def eval(model, n, val_series, num_samples=2):
    """
    Evaluate the trained model with validation data.
    """
    pred_series = model.predict(n=n, num_samples=num_samples)
    return mape(val_series, pred_series)
