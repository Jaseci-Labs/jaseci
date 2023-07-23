import pandas as pd
import numpy as np

from darts.dataprocessing.transformers import Scaler
from darts import TimeSeries, concatenate


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


def create_covariates(series):
    pass
