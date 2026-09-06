def xt(t, uk, vTk, x0, lk):
    if vTk.size != x0.size:
        return None
    vTk = Transpose(vTk)
    x0 = toColumnVector(x0)
    Dk = (vTk @ x0)[0]
    return uk * (Dk) * np.exp(lk*t)


def formSolution(tspace,eigvals,eigvecs,vT):
    X = [[]] * len(eigvals)
    x0 = np.array([1.0, 0.0, -1.0])
    
    for j in range(tspace.size):
        s = np.zeros_like(x0)
        for i in range(len(eigvals)):
            s += xt(tspace[j], eigvecs[:,i], vT[:,i],x0,eigvals[i])
        for k in range(len(eigvals)):
            X[k].append(s[k])
    return np.array(X)