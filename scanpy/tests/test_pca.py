import scanpy as sc
import numpy as np
import pytest
from scipy.sparse import csr_matrix

A_list = [
    [0, 0, 7, 0, 0],
    [8, 5, 0, 2, 0],
    [6, 0, 0, 2, 5],
    [0, 0, 0, 1, 0],
    [8, 8, 2, 1, 0],
    [0, 0, 0, 4, 5]
]

A_pca = np.array([
    [-4.4783009 ,  5.55508466,  1.73111572, -0.06029139,  0.17292555],
    [ 5.4855141 , -0.42651191, -0.74776055, -0.74532146,  0.74633582],
    [ 0.01161428, -4.0156662 ,  2.37252748, -1.33122372, -0.29044446],
    [-3.61934397,  0.48525412, -2.96861931, -1.16312545, -0.33230607],
    [ 7.14050048,  1.86330409, -0.05786325,  1.25045782, -0.50213107],
    [-4.53998399, -3.46146476, -0.32940009,  2.04950419,  0.20562023]
])

A_svd = np.array([
    [-0.77034038, -2.00750922,  6.64603489, -0.39669256, -0.22212097],
    [-9.47135856, -0.6326006 , -1.33787112, -0.24894361, -1.02044665],
    [-5.90007339,  4.99658727,  0.70712592, -2.15188849,  0.30430008],
    [-0.19132409,  0.42172251,  0.11169531,  0.50977966, -0.71637566],
    [-11.1286238, -2.73045559,  0.08040596,  1.06850585,  0.74173764],
    [-1.50180389,  5.56886849,  1.64034442,  2.24476032, -0.05109001]
])

@pytest.mark.parametrize('typ', [np.array, csr_matrix])
def test_pca_transform(typ):
    A = typ(A_list, dtype='float32')
    A_pca_abs = np.abs(A_pca)
    A_svd_abs = np.abs(A_svd)

    adata = sc.AnnData(A)

    sc.pp.pca(adata, n_comps=4, zero_center=True, svd_solver='arpack', dtype='float64')

    assert np.linalg.norm(A_pca_abs[:, :4]-np.abs(adata.obsm['X_pca'])) < 2e-05

    sc.pp.pca(adata, n_comps=5, zero_center=True, svd_solver='randomized',
              dtype='float64', random_state=14)
    assert np.linalg.norm(A_pca_abs-np.abs(adata.obsm['X_pca'])) < 2e-05

    sc.pp.pca(adata, n_comps=4, zero_center=False, dtype='float64', random_state=14)
    assert np.linalg.norm(A_svd_abs[:, :4]-np.abs(adata.obsm['X_pca'])) < 2e-05
