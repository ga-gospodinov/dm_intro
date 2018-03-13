import numpy as np


def matrix_multiply(X, Y):
    """ Matrix multiplication
    Inputs:
      - X: A numpy array of shape (N, M)
      - Y: A numpy array of shape (M, K)
    Output:
      - out: A numpy array of shape (N, K)
    """
    out = np.dot(X, Y)
    return out


def matrix_rowmean(X, weights=np.empty(0)):
    """ Calculate mean of each row.
    In case of weights do weighted mean.
    For example, for matrix [[1, 2, 3]] and weights [0, 1, 2]
    weighted mean equals 2.6666 (while ordinary mean equals 2)
    Inputs:
      - X: A numpy array of shape (N, M)
      - weights: A numpy array of shape (M,) or an emty array of shape (0,)
    Output:
      - out: A numpy array of shape (N,)
    """
    if weights.size:
        out = np.average(X, axis=1, weights=weights)
    else:
        out = np.mean(X, axis=1)
    return out


def cosine_similarity(X, top_n=10, with_mean=True, with_std=True):
    """ Calculate cosine similarity between each pair of row.
    1. In case of with_mean: subtract mean of each row from row
    2. In case of with_std: divide each row on it's std
    3. Select top_n best elements in each row or set other to zero.
    4. Compute cosine similarity between each pair of rows.
    Inputs:
      - X: A numpy array of shape (N, M)
      - top_n: int, number of best elements in each row
      - with_mean: bool, in case of subtracting each row's mean
      - with_std: bool, in case of subtracting each row's std
    Output:
      - out: A numpy array of shape (N, N)

    Example (with top_n=1, with_mean=True, with_std=True):
        X = array([[1, 2], [4, 3]])
        after mean and std transform:
        X = array([[-1.,  1.], [ 1., -1.]])
        after top n choice
        X = array([[0.,  1.], [ 1., 0]])
        cosine similarity:
        X = array([[ 1.,  0.], [ 0.,  1.]])

    """
    if with_mean:
        X = X - np.mean(X, axis=1).reshape(X.shape[0], 1)
    if with_std:
        X = X / np.std(X, axis=1).reshape(X.shape[0], 1)
    col = np.argsort(X)[:, :X.shape[1] - top_n]
    for (ndx, c) in enumerate(col):
        X[ndx, col[ndx]] = np.zeros(X.shape[1] - top_n)
    norm = (X * X).sum(axis=1, keepdims=True) ** 0.5
    out = np.dot(X, X.T) / norm / norm.T
    return out
