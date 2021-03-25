import numpy as np


def cosine_sim(param_list):
    """
    Caculate the cosine similarity score of two given vectors
    Param 1 - First vector
    Param 2 - Second vector

    Return - float between 0 and 1
    """
    vec_a = param_list[0]
    vec_b = param_list[1]

    return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))


def dot_product(param_list):
    """
    Caculate the dot product of two given vectors
    Param 1 - First vector
    Param 2 - Second vector

    Return - float between 0 and 1
    """

    return np.inner(param_list[0], param_list[1])


def get_centroid(param_list):
    """
    Calculate the centroid of the given list of vectors
    Param 1 - List of vectors

    Return - (centroid vector, cluster tightness)
    """
    vec_list = param_list[0]
    centroid = np.mean(vec_list, axis=0)
    tightness= np.mean([cosine_sim([vec, centroid]) for vec in vec_list])
    return (centroid, tightness)
