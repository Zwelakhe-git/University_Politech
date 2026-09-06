#singularDecomposition.py
import numpy as np
import initsyalizatsyaMatristy as im
import QR_algorithm as qr
import HouseholderTransformation as hh

def decompose(A, iterations=100):
    B = A @ A.T
    B_diag = qr.calculate(B,iterations)
    eigvals = np.array([i for i in np.diag(B_diag)])
    eigvals = np.clip(eigvals, 0, None)
    eigvals = np.sqrt(eigvals)

    eigvals_full, U = np.linalg.eigh(B)
    sorted_indices = np.argsort(-np.sqrt(np.clip(eigvals_full, 0, None)))
    U = U[:, sorted_indices]
    eigvals_sorted = eigvals[sorted_indices]

    tol = 1e-10
    none_zero = eigvals_sorted > tol
    U = U[:, none_zero]

    V = A.T @ A
    V = V / eigvals_sorted[1:]

    SIG = np.zeros_like(A, dtype=float)
    r = min(SIG.shape[0], SIG.shape[1], len(eigvals_sorted))
    for i in range(r):
        SIG[i, i] = eigvals_sorted[i]

    return U, SIG, V

m = im.A.shape[0]
A = im.A.copy()[:, :m-1]

U, SIG, V = decompose(A)
A_reconstr = U @ SIG @ V.T
print(A, A_reconstr, sep="\n")
print("погрешность восстанавления: ", np.linalg.norm(A - A_reconstr))

