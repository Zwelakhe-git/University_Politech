import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

p1 = 8.4e-6
p2 = 6.6667e-4
p3 = 1.7778e-5
p5 = 2

# Увеличенный диапазон значений p4 и p6
grid_size = 10
p4_values = np.logspace(-1, 1, grid_size)
p6_values = np.logspace(-1, 1, grid_size)

def function(x3, p4, p6):
    denominator = (-p1 - (x3 + p4 * x3)) / p3 - p4
    if np.any(denominator == 0):
        return np.inf
    return (((-p4*p6 - p5*x3/p3) / denominator) * (p1 - (x3 + p4 * x3)) + 
            (x3 + p4 * x3) * (1 - (x3 + p4 * x3))) / p2 - p4 * (x3 + p4 * x3)

def getX1(x3, p4):
    return x3 + p4 * x3

def getX2(x1, x3, p4, p6):
    denominator = (-p1 - x1) / p3 - p4
    valid = denominator != 0
    x2 = np.full_like(x1, np.nan)
    x2[valid] = (-p4 * p6 - p5 * x3[valid] / p3) / denominator[valid]
    return x2

def jacobian(x1,x2,p4,p6):
    ustoychivy = []
    if len(x1) == len(x2):
        l = len(x1)
        for i in range(l):
            J = [[(-x2[i] + 1 - 2*x1[i])/p2 - p4, (p1 - x1[i])/p2, 0],
         [-x2[i]/p3, (-p1 - x1[i])/p3 - p4, p5/p3],
         [1, 0, -(1 + p4)]]
            
            eigs = np.linalg.eigvals(J)
            if np.all(eigs < 0):
                ustoychivy.append([x1[i],x2[i]])

    return ustoychivy
    

# Улучшенный выбор начальных приближений
initial_guesses = np.linspace(-5, 5, 10)

num_solutions = np.zeros((grid_size, grid_size))
station_roots = {}
for i, p4 in enumerate(p4_values):
    for j, p6 in enumerate(p6_values):
        roots = fsolve(function, initial_guesses, args=(p4, p6))
        unique_roots = np.unique(np.round(roots, 9))
        num_solutions[i, j] = len(unique_roots)

        X1 = getX1(unique_roots,p4)
        X2 = getX2(X1,unique_roots,p4,p6)

        station_roots[(p4,p6)] = jacobian(X1,X2,p4,p6)
        

# Построение бифуркационной диаграммы

plt.figure(figsize=(8, 6))
c = plt.contourf(np.log10(p4_values), np.log10(p6_values), num_solutions.T, levels=np.arange(1, np.max(num_solutions) + 1), cmap='viridis')
#strm = plt.streamplot(np.log10(p4_values), np.log10(p6_values), trans[0],trans[1],color=trans,cmap='uatumn')
plt.colorbar(c, label='Количество решений')
plt.xlabel('log(p4)')
plt.ylabel('log(p6)')
plt.title('Бифуркационная диаграмма стационарных точек')
plt.show()

