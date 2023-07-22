import optuna

import pandas as pd
import numpy as np

from darts.dataprocessing.transformers import Scaler
from darts import TimeSeries, concatenate


transformer = Scaler()


def create_series(time: list, variables: dict):
    """ """
    dataframe = pd.DataFrame.from_dict(variables)
    dataframe["time"] = time
    dataframe["time"] = dataframe["time"].apply(lambda x: pd.to_datetime(x))
    dataframe.set_index("time", inplace=True)
    series = TimeSeries.from_times_and_values(times=dataframe.index, values=dataframe)
    series = series.astype(np.float32)
    return series
