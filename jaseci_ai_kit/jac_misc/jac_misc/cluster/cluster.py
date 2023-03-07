import json
import umap
import hdbscan

import numpy as np

import sklearn.cluster as cluster

from jaseci.actions.live_actions import jaseci_action
from jaseci.actions.remote_actions import launch_server
from fastapi import HTTPException


def get_umap_embedds(
    text_embeddings: list, n_neighbors=15, min_dist=0.1, n_components=2, random_state=42
):
    """
    Dimentionality reduction using umap
    Parameters:
    -----------
    text_embeddings: json object of embeddings.
    n_neighbors: integer
    min_dist: float
    n_components: integer
    random_state: integer
    Return:
    -----------
    clusterable_embedds: ndarray, dimentionality reduced (by umap algorithm) multidimentional array
    """
    emb_str = str(text_embeddings)
    emb_array = np.array(json.loads(emb_str))

    clusterable_embedds = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        n_components=n_components,
        random_state=random_state,
    ).fit_transform(emb_array)

    return clusterable_embedds.tolist()


def hbdscan_clustering(embeddings, min_samples, min_cluster_size):
    """
    Clustering using hbdscan
    Parameters:
    -----------
    embeddings: ndarray, list of embeddings.
    min_samples: integer.
    min_cluster_size: integer.
    Return:
    -----------
    labels: array of integer, containing correspondant class of each input embeddings
    """

    labels = hdbscan.HDBSCAN(
        min_samples=min_samples, min_cluster_size=min_cluster_size
    ).fit_predict(embeddings)

    return labels


def kmeans_clustering(embeddings, n_clusters):
    """
    Clustering using kmeans algorithm.

    Parameters:
    -----------
    embeddings: ndarray, list of embeddings.
    n_clusters: number of clusters.

    Return:
    -----------
    labels: array of integer, containing correspondant class of each input embeddings
    """
    labels = cluster.KMeans(n_clusters=n_clusters).fit_predict(embeddings)
    print(labels)
    return labels


@jaseci_action(act_group=["cluster"], allow_remote=True)
def get_umap(
    text_embeddings: list,
    n_neighbors: int = 15,
    min_dist: float = 0.1,
    n_components: int = 2,
    random_state: int = 42,
):
    try:
        umap_embedds = get_umap_embedds(
            text_embeddings=text_embeddings,
            n_neighbors=n_neighbors,
            min_dist=min_dist,
            n_components=n_components,
            random_state=random_state,
        )
        return umap_embedds
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


VALID_ALGOS = {"hbdscan", "kmeans"}
KMEANS_PARAMS = {"n_clusters"}
HBDSCAN_PARAMS = {"min_samples", "min_cluster_size"}


@jaseci_action(act_group=["cluster"], allow_remote=True)
def get_cluster_labels(
    embeddings: list,
    algorithm: str = "hbdscan",
    min_samples: int = None,
    min_cluster_size: int = None,
    n_clusters: int = None,
):
    if algorithm not in VALID_ALGOS:
        raise ValueError("the algorithm must be one of %r." % VALID_ALGOS)
    elif algorithm == "hbdscan":
        if min_samples is None:
            raise ValueError(
                "If you are using hbdscan algorith min_samples should be defined"
            )
        elif min_cluster_size is None:
            raise ValueError(
                "If you are using hbdscan algorith min_cluster_size should be defined"
            )
        else:
            try:
                cluster_labels = hbdscan_clustering(
                    embeddings=embeddings,
                    min_samples=min_samples,
                    min_cluster_size=min_cluster_size,
                )
                return cluster_labels.tolist()
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    elif algorithm == "kmeans":
        if n_clusters is None:
            raise ValueError(
                "If you are using kmeans algorithm n_clusters should be defined"
            )
        else:
            try:
                cluster_labels = kmeans_clustering(
                    embeddings=embeddings,
                    n_clusters=n_clusters,
                )
                return cluster_labels.tolist()
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("The text cluster module is up and running.")
    launch_server(port=8000)
