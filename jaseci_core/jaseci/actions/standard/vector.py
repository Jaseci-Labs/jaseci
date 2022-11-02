"""Built in actions for Jaseci"""
import numpy as np
from operator import itemgetter
from jaseci.actions.live_actions import jaseci_action



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
