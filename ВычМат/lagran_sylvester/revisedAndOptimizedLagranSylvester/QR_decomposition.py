import numpy as np
import initsyalizatsyaMatristy as im
import Tests

def transform(A):
    m = A.shape[0]
    Q = np.eye(m)
    
    for i in range(m - 1):
        x = A[i:,i]
        e = np.zeros_like(x)
        e[0] = 1
        v = x + np.linalg.norm(x)*e
        v = v / np.linalg.norm(v)

        H = np.eye(m - i) - 2 * (v.reshape(-1,1) @ v.reshape(1,-1))
        if i == 0:
            U = H
            A = U @ A
        else:
            U = np.eye(m)
            U[i:, i:] = H
            A = U @ A
        Q = U @ Q
    return Q.T, A

"""A = im.A.copy()
Q, R = transform(A)
print(Q, R, sep='\n')

print(f"A = QR: {np.allclose(im.A, Q @ R)}")
print(f"Q.T @ Q = E: {np.allclose(Q.T @ Q, np.eye(Q.shape[0]))}")
print(f"Q isHessenberg: {Tests.isHessenberg(Q)}")
print(f"R isUpperTriangular: {Tests.isUpperTriangular(R)}")
print(f"Q isSimmetrical: {Tests.symmetryTest(Q)}")"""