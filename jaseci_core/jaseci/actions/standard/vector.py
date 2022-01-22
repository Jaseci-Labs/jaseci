"""Built in actions for Jaseci"""
import numpy as np
from operator import itemgetter


def cosine_sim(param_list, meta):
    """
    Caculate the cosine similarity score of two given vectors
    Param 1 - First vector
    Param 2 - Second vector

    Return - float between 0 and 1
    """
    vec_a = param_list[0]
    vec_b = param_list[1]

    result = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) *
                                     np.linalg.norm(vec_b))
    return result.astype(float)


def dot_product(param_list, meta):
    """
    Caculate the dot product of two given vectors
    Param 1 - First vector
    Param 2 - Second vector

    Return - float between 0 and 1
    """

    return np.inner(param_list[0], param_list[1])


def get_centroid(param_list, meta):
    """
    Calculate the centroid of the given list of vectors
    Param 1 - List of vectors

    Return - (centroid vector, cluster tightness)
    """
    vec_list = param_list[0]
    centroid = np.mean(vec_list, axis=0)
    tightness = np.mean([cosine_sim([vec, centroid], meta)
                         for vec in vec_list]).astype(float)
    return [centroid, tightness]


def softmax(param_list, meta):
    """
    Calculate the centroid of the given list of vectors
    Param 1 - List of vectors

    Return - (centroid vector, cluster tightness)
    """
    vec_list = param_list[0]
    e_x = np.exp(vec_list - np.max(vec_list))
    return list(e_x / e_x.sum())


def sort_by_key(param_list, meta):  # TODO: Should be in std lib
    """
    Sort the given list. Optionally by specific key
    Param 1 - List of items
    Param 2 - if Reverse
    Param 2 (Optional) - Index of the key to be used for sorting
    if param 1 is a list of tuples.
    """
    data = param_list[0]
    if_reverse = param_list[1]

    if (len(param_list) > 2):
        key_pos = param_list[2]
        return sorted(data, key=itemgetter(key_pos), reverse=if_reverse)
    else:
        return sorted(data, reverse=if_reverse)
