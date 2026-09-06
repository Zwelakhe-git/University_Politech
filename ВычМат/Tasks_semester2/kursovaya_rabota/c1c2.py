import numpy as np
import scipy.integrate as spi
import scipy.optimize as opt

# Вычисление c1
def integrand(z):
    return z / (np.sin(z) * (np.cos(z) + 0.8 * np.sin(z)))

c1_factor = 0.6087475
c1, _ = spi.quad(integrand, 0, np.pi/2)
c1 *= float(f"{c1_factor:.5f}")

# Найдем отрицательный корень уравнения e^x + e^(-3x) = 4
def equation(x):
    #return (x**2 + 1)**2 - x + 1
    return np.exp(x) + np.exp(-3 * x) - 4

x_star = opt.root_scalar(equation, bracket=[-2, 1]).root

# Вычисление c2
c2_factor = -2.493594
c2 = c2_factor * float(f"{x_star:.5f}")
#print(c1,"\nxstart",float(f"{x_star:.5f}"))
#========================================


# Определим систему уравнений первого порядка
def dydt(t, Y, c1, c2):
    y, v = Y  # y = Y[0], v = Y[1] = dy/dt
    dy_dt = v
    dv_dt = c1 * y / (1 + y**2)**3 - c2 * v
    return [dy_dt, dv_dt]

# Начальные условия
y0 = [0.05, 0]  # y(0) = 0.05, y'(0) = 0
t_span = (0, 1)  # Интервал интегрирования
t_eval = np.linspace(0, 1, 100)  # Точки для вычисления

# Численное решение с RK45
sol = spi.solve_ivp(dydt, t_span, y0, args=(c1, c2), t_eval=t_eval, method='RK45')

# Построим график решения
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.plot(sol.t, sol.y[0], label=r"$y(t)$", color="b")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.title("Решение дифференциального уравнения")
plt.legend()
plt.grid()
plt.show()

