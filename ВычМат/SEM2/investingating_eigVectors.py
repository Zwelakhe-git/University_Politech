import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi


def SOE(t,Y):
    x,y,z = Y
    dxdt = -5*x -2*y -2*z
    dydt = 10*x + 4*y + 2*z
    dzdt = 2*x + y + 3*z

    return [dxdt,dydt,dzdt]

systemMatrix = np.array([
    [-5, -2, -2],[10, 4, 2],[2, 1, 3]
])
eigs = np.linalg.eigvals(systemMatrix)
eigsT = np.linalg.eigvals(systemMatrix.T)

#собственные векторы одному собственному значению различаются
u1 = np.array([2, -8, 2])
u1T = np.array([2, 1, 1])
u2T = np.array([2, 1, 2])

t_span = (0,3)
t_eval = np.linspace(*t_span,300)
NU = [2, -8, 2]

print("u1 = {0}, u1T = {1}".format(u1, u1T))
print("$\\lambda_1 = {0}$".format(eigs[1]))
print("$Au1 = {0}$".format(systemMatrix @ u1))
print("$A^T u1T = {0}$".format(systemMatrix.T @ u1T))
print("u1T^T A = {0}".format(u1T.T @ systemMatrix))
print("$u1^T * u1T = {0}, u1T^T * u1 = {1}$".format(u1.T @ u1T, u1T.T @ u1))

sol = spi.solve_ivp(SOE,t_span,NU,t_eval=t_eval)
solT = spi.solve_ivp(SOE,t_span,u1T,t_eval=t_eval)

ax = plt.figure().add_subplot(projection='3d')
ax.plot(sol.y[0],sol.y[1],sol.y[2],label='f(x,y,z)')
ax.plot(solT.y[0],solT.y[1],solT.y[2],c='r')
ax.set_title('траектория в пространстве')
ax.legend()

plt.show()
