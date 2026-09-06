import numpy as np
from scipy.optimize import fsolve

# Определяем функцию f(x) = x^4 + 2x^2 - x + 2
def equation(x):
    return x**4 + 2*x**2 - x + 2

# Начальное приближение для корней
initial_guesses = [-2, -1, 0, 1, 2]

# Находим корни уравнения
roots = fsolve(equation, initial_guesses)

# Оставляем только уникальные вещественные корни
unique_roots = np.unique(np.round(roots, 6))

x = unique_roots[0]
y = x**2 + 1

print(x,y)

J = np.array([[2 * x,-1],[-1,2*y]])

eigs = np.linalg.eigvals(J)
print(eigs)
