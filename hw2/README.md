# Results

|        |    1   |    2   |    3   |
|--------|--------|--------|--------|
| numpy  |  16 ms | 4 ms   | 1.46 s |
| numba  |  96 ms | 0.48 ms| 17.3 s |
| cython |  96 ms | 65 ms  | 13.9 s |

1 - matrix_multiply
2 - matrix_rowmean
3 - cosine_similarity