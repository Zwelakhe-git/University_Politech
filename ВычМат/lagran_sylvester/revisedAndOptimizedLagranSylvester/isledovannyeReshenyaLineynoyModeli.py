import numpy as np
import matplotlib.animation as animation
import initsyalizatsyaMatristy as im
from SetGraph import *

def init():
    ax.set_xlim(-1.5, 2.5)
    ax.set_ylim(-1.5, 2.5)
    del x1[:]
    del x2[:]
    del x3[:]
    del tdata[:]
    line, = ax.plot([],[], lw=1, label="x(t)")
    line2, = ax.plot([],[], lw=1, label="y(t)")
    line3, = ax.plot([],[], lw=1, label="z(t)")
    return line

def run(data):
    x,y,z,t = data
    x1.append(x)
    x2.append(y)
    x3.append(z)
    tdata.append(t)
    #print(t)

    ax.set_title(f"t: {t:.2f}, ymax: {max([x,y,z]):.2f}")
    ymin, ymax = ax.get_ylim()
    xmin, xmax = ax.get_xlim()
    if t > xmax:
        ax.set_xlim(xmin, 2*xmax)
    if max([x,y,z]) > ymax:
        ax.set_ylim(ymin, 2*ymax)
        ax.set_xlim(ymin, 2*ymax)

    ax.figure.canvas.draw()
    line.set_data(x1,t)
    line2.set_data(x2,t)
    line3.set_data(x3,t)
    
    return line,

def Transpose(v):
    return v.reshape(1, -1)

def toColumnVector(v):
    return v.reshape(-1, 1)        

def formSolution(tspace, eigvals, eigvecs, vT, x0):
    n = eigvecs.shape[0]     # размерность пространства
    m = eigvals.size         # число собственных значений

    X = np.zeros((n, tspace.size))  # итоговая матрица X[:,j] = x(t_j)

    # Вычисляем коэффициенты v_k^T x0 для всех k заранее
    coeffs = np.array([vT[:,k] @ x0 for k in range(m)])

    for idx, t in enumerate(tspace):
        exp_lambda_t = np.exp(eigvals * t)  # массив e^{lambda_k * t} для всех k
        x_t = eigvecs @ (coeffs * exp_lambda_t)  # быстро: линейная комбинация u_k
        X[:, idx] = x_t

    return X

    
tspace = np.linspace(0, 2, 100)
x0 = np.array([1.0, 0.0, -1.0])
A = im.B
AT = A.T

eigvals, eigvecs = np.linalg.eig(A)
eigvT,vT = np.linalg.eig(AT)

swapIndx = [0] * len(eigvals)
for i,v in enumerate(eigvals):
    indx = np.round(eigvT,2).tolist().index(np.round(v,2))
    swapIndx[indx] = i

for i,indx in enumerate(swapIndx):
    if i == indx:
        continue
    vT[:,[i, indx]] = vT[:,[indx, i]]
    swapIndx[indx] = indx

# >>> нормируем векторы <<<
for i in range(eigvals.size):
    vTi = vT[:, i].reshape(1, -1)        # строка
    uKi = eigvecs[:, i].reshape(-1, 1)    # столбец
    scale = (vTi @ uKi)[0, 0]             # скаляр v^T u
    vT[:, i] /= scale

X = formSolution(tspace=tspace, eigvals=eigvals,eigvecs=eigvecs,vT=vT,x0=x0)

#ani = animation.FuncAnimation(fig, run, frames=zip(X[0],X[1],X[2],tspace),init_func=init)
#plt.show()
print("t,x1,x2,x3")
for i in range(3):
    print("%.2e,%.4e,%.4e,%.4e"%(tspace[i],X[0][i],X[1][i],X[2][i]))
