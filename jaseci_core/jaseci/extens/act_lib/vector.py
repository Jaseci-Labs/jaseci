"""Built in actions for Jaseci"""
import numpy as np
from operator import itemgetter
import pickle, base64

from jaseci.jsorc.live_actions import jaseci_action


def check_nested_list(lst):
    return all(isinstance(el, list) for el in lst)


@jaseci_action(aliases=["cos_sim"])
def cosine_sim(vec_a: list, vec_b: list):
    """
    Caculate the cosine similarity score of two given vectors
    Param 1 - First vector
    Param 2 - Second vector

    Return - float between 0 and 1
    """
    vec_a_nested = check_nested_list(vec_a)
    vec_b_nested = check_nested_list(vec_b)
    if vec_a_nested or vec_b_nested:
        vec_a_np = np.array(vec_a) if vec_a_nested else np.array([vec_a] * len(vec_b))
        vec_b_np = np.array(vec_b) if vec_b_nested else np.array([vec_b] * len(vec_a))
        sim = np.dot(vec_a_np, vec_b_np.T) / (
            np.linalg.norm(vec_a_np, axis=1)[:, None] * np.linalg.norm(vec_b_np, axis=1)
        )
        return sim.diagonal().tolist()

    result = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
    return float(result.astype(float))


@jaseci_action()
def dot_product(vec_a: list, vec_b: list):
    """
    Caculate the dot product of two given vectors
    Param 1 - First vector
    Param 2 - Second vector

    Return - float between 0 and 1
    """

    return np.inner(vec_a, vec_b).tolist()


@jaseci_action()
def get_centroid(vec_list: list):
    """
    Calculate the centroid of the given list of vectors
    Param 1 - List of vectors

    Return - (centroid vector, cluster tightness)
    """
    centroid = np.mean(vec_list, axis=0)
    tightness = np.mean([cosine_sim(vec, centroid) for vec in vec_list]).astype(float)
    return [centroid.tolist(), tightness]


@jaseci_action()
def softmax(vec_list: list):
    """
    Calculate the centroid of the given list of vectors
    Param 1 - List of vectors

    Return - (centroid vector, cluster tightness)
    """
    e_x = np.exp(vec_list - np.max(vec_list))
    return list(e_x / e_x.sum())


@jaseci_action()
def sort_by_key(data: dict, reverse=False, key_pos=None):
    """
    Sort the given list. Optionally by specific key
    Param 1 - List of items
    Param 2 - if Reverse
    Param 3 (Optional) - Index of the key to be used for sorting
    if param 1 is a list of tuples.

    Deprecated
    """
    if key_pos is not None:
        return sorted(data, key=itemgetter(key_pos), reverse=reverse)
    else:
        return sorted(data, reverse=reverse)


@jaseci_action()
def dim_reduce_fit(data: list, dim=2):
    """
    Dimensionally reduce a list of vectors using incremental PCA
    Param 1 - List of vectors
    Param 2 - Dimension to reduce to

    Return - base64 encoded string of the model
    """
    data_arr = np.array(data)
    ipca = IncrementalPCA(n_components=dim)
    ipca = ipca.fit(data_arr)
    return base64.b64encode(pickle.dumps(ipca)).decode("utf-8")


@jaseci_action()
def dim_reduce_apply(data: list, model: str):
    """
    Dimensionally reduce a list of vectors using incremental PCA
    Param 1 - List of vectors
    Param 2 - base64 encoded string of the model

    Return - List of reduced vectors
    """
    data_arr = np.array(data)
    # reshaping the data if it is a single vector
    if len(data_arr.shape) == 1:
        data_arr = data_arr.reshape(1, -1)
    ipca = pickle.loads(base64.b64decode(model))
    return ipca.transform(data_arr).tolist()


class IncrementalPCA:
    def __init__(self, n_components):
        self.n_components = n_components
        self.mean_ = None
        self.components_ = None
        self.n_samples_seen_ = 0

    def fit(self, X):
        if self.mean_ is None:
            self.mean_ = np.zeros(X.shape[1], dtype=np.float64)
        if self.components_ is None:
            self.components_ = np.zeros(
                (self.n_components, X.shape[1]), dtype=np.float64
            )

        # update mean
        col_mean = np.mean(X, axis=0)
        total_n_samples = self.n_samples_seen_ + X.shape[0]
        self.mean_ = (
            self.n_samples_seen_ * self.mean_ + X.shape[0] * col_mean
        ) / total_n_samples

        # update components
        X_centered = X - self.mean_
        U, S, V = np.linalg.svd(X_centered, full_matrices=False)
        explained_variance = S**2 / (X.shape[0] - 1)
        explained_variance_ratio = explained_variance / np.sum(explained_variance)
        self.components_ = V[: self.n_components]
        self.n_samples_seen_ = total_n_samples

        return self

    def transform(self, X):
        X_centered = X - self.mean_
        return np.dot(X_centered, self.components_.T)
