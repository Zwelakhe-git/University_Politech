import numpy as np
import initsyalizatsyaMatristy as im

def givens_rotation(a, b):
    r = np.hypot(a, b)
    c = a / r
    s = -b / r
    return c, s

def to_hessenberg(A):
    A = A.copy()
    n = A.shape[0]
    file = open("givensTransformation.log","w")
    for j in range(n - 2):
        for i in range(n - 1, j + 1, -1):
            a = A[i-1, j]
            b = A[i, j]
            if b != 0:
                c, s = givens_rotation(a, b)
                strng = f"A:{A}\n\na_jj=A[{i},{j+1}]={A[i-1,j]}, a_kj=A[{i+1},{j+1}]={A[i,j]}\n"
                strng += f"r = {np.hypot(a, b)}\n"

                G = np.eye(n)
                G[[i-1, i], [i-1, i]] = c
                G[i, i-1] = s
                G[i-1, i] = -s

                A = G @ A @ G.T  # сохраняем симметрию, если нужно
                file.write(strng + f"s=-a_kj/r={s},c=a_jj/r={c}\n\nT{i+1}{i}\n{G}\n\n")
    file.close()
    return A

to_hessenberg(im.A)