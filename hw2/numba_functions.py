from numba import jit
import numpy as np


@jit(nopython=True)
def matrix_multiply(X, Y):
    """ Matrix multiplication
    Inputs:
      - X: A numpy array of shape (N, M)
      - Y: A numpy array of shape (M, K)
    Output:
      - out: A numpy array of shape (N, K)
    """
    out = np.zeros((X.shape[0], Y.shape[1]))
    for i in range(X.shape[0]):
        for j in range(Y.shape[1]):
            for k in range(X.shape[1]):
                out[i, j] += X[i, k] * Y[k, j]
    return out


@jit(nopython=True)
def matrix_rowmean(X, weights=np.empty(0)):
    """ Calculate mean of each row.
    In case of weights do weighted mean.
    For example, for matrix [[1, 2, 3]] and weights [0, 1, 2]
    weighted mean equals 2.6666 (while ordinary mean equals 2)
    Inputs:
      - X: A numpy array of shape (N, M)
      - weights: A numpy array of shape (M,)
    Output:
      - out: A numpy array of shape (N,)
    """
    weights_sum = 0.0
    out = np.zeros(X.shape[0])
    if weights.size:
        for i in range(weights.shape[0]):
            weights_sum += weights[i]
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                out[i] += X[i, j] * weights[j]
            out[i] /= weights_sum
    else:
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                out[i] += X[i, j]
            out[i] /= X.shape[1]
    return out


@jit(nopython=True)
def mean(a):
    n = a.shape[0]
    m = 0.0
    for i in range(n):
        m += a[i]
    return m / n


@jit(nopython=True)
def std(a):
    n = a.shape[0]
    m = mean(a)
    v = 0.0
    for i in range(n):
        v += (a[i] - m)**2
    return (v / n)**0.5


@jit
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
    n = X.shape[0]
    k = X.shape[1]
    if with_mean:
        for i in range(n):
            m = mean(X[i])
            for j in range(k):
                X[i, j] = X[i, j] - m
    if with_std:
        for i in range(n):
            s = std(X[i])
            for j in range(k):
                X[i, j] = X[i, j] / s
    for i in range(n):
        num_to_delete = k - top_n
        index = np.argpartition(X[i], num_to_delete)
        for j in range(num_to_delete):
            X[i, index[j]] = 0.0
    out = np.zeros((X.shape[0], X.shape[0]))
    for i in range(n):
        for j in range(n):
            ab = 0.0
            norm_a = 0.0
            norm_b = 0.0
            for d in range(k):
                ab += X[i, d] * X[j, d]
                norm_a += X[i, d] ** 2
                norm_b += X[j, d] ** 2
            out[i, j] = ab / (norm_a ** 0.5) / (norm_b ** 0.5)
    return out
