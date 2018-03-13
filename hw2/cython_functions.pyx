import numpy as np
cimport numpy as np
cimport cython

cdef extern from "math.h":
    double sqrt(double m)


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef matrix_multiply(np.ndarray[np.float64_t, ndim=2] X,
                      np.ndarray[np.float64_t, ndim=2] Y):
    """ Matrix multiplication
    Inputs:
      - X: A numpy array of shape (N, M)
      - Y: A numpy array of shape (M, K)
    Output:
      - out: A numpy array of shape (N, K)
    """
    cdef np.ndarray[np.float64_t, ndim = 2] out = np.zeros((X.shape[0], Y.shape[1]), dtype=np.float64)
    for i in range(X.shape[0]):
        for j in range(Y.shape[1]):
            for k in range(X.shape[1]):
                out[i, j] += X[i, k] * Y[k, j]
    return out


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef matrix_rowmean(X, weights=np.empty(0)):
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
    cdef np.float64_t weights_sum = 0.0
    cdef np.ndarray[np.float64_t, ndim = 1] out = np.zeros(X.shape[0], dtype=np.float64)
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


@cython.boundscheck(False)
@cython.cdivision(True)
cdef double mean(double[:] a):
    cdef size_t i
    cdef size_t n = a.shape[0]
    cdef double m = 0.0
    for i in range(n):
        m += a[i]
    return m / n


@cython.boundscheck(False)
@cython.cdivision(True)
cdef double std(double[:] a):
    cdef size_t i
    cdef size_t n = a.shape[0]
    cdef double m = mean(a)
    cdef double v = 0.0
    for i in range(n):
        v += (a[i] - m)**2
    return sqrt(v / n)


@cython.boundscheck(False)
@cython.cdivision(True)
cpdef np.ndarray[np.float64_t, ndim = 2] cosine_similarity(np.ndarray[np.float64_t, ndim=2] X,
                                                           size_t top_n=10, bint with_mean=True, bint with_std=True):
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
    cdef size_t i, j
    cdef size_t n = X.shape[0]
    cdef size_t k = X.shape[1]
    cdef double m, s
    cdef size_t num_to_delete
    cdef long[:] index
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
    cdef np.ndarray[np.float64_t, ndim = 2] out = np.zeros((X.shape[0], X.shape[0]), dtype=np.float64)
    cdef double ab = 0.0
    cdef double norm_a = 0.0
    cdef double norm_b = 0.0
    for i in range(n):
        for j in range(n):
            ab = 0.0
            norm_a = 0.0
            norm_b = 0.0
            for d in range(k):
                ab += X[i, d] * X[j, d]
                norm_a += X[i, d] ** 2
                norm_b += X[j, d] ** 2
            out[i, j] = ab / sqrt(norm_a) / sqrt(norm_b)
    return out
