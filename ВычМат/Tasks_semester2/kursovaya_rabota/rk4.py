import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


fig,axs = plt.subplots(2,1,figsize=(9, 7),height_ratios=[3,1])
axs = axs.flat
# Дифференциальное уравнение

def bubble_dynamics(t, Y, c1, c2):
    y, v = Y
    dydt = v
    dvdt = -c2 * v + c1 * y / (1 + y**2)**3
    return [dydt, dvdt]

# Заданные параметры
c1 = 0.99999 #9727870315  # Интеграл, верхний предел pi/2
c2 = 1.0000  # Найденный корень уравнения e^x + e^(-3x) = 4

# Начальные условия
#y0 = [0.05, 0]
eps = 5e-7
y0 = [0.05, 0]  # (y(0), y'(0))
epsy0 = [y - eps for y in y0]

t_span = (0, 1)  # Интервал времени
t_eval = np.linspace(0, 1, 100)  # Точки для вычисления

# Решение методом RK45
sol_rk45 = solve_ivp(bubble_dynamics, t_span, y0, args=(c1, c2), t_eval=t_eval, method='RK45')
epsSol_rk45 = solve_ivp(bubble_dynamics, t_span, epsy0, args=(c1, c2), t_eval=t_eval, method='RK45')

# Решение методом RK4 (фиксированный шаг)
def rk4_step(f, t, Y, h, c1, c2):
    k1 = np.array(f(t, Y, c1, c2))
    k2 = np.array(f(t + h/2, Y + h*k1/2, c1, c2))
    k3 = np.array(f(t + h/2, Y + h*k2/2, c1, c2))
    k4 = np.array(f(t + h, Y + h*k3, c1, c2))
    return Y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)

# Численное решение методом RK4
def solve_rk4(f, t_span, y0, c1, c2, n=100):
    t_values = np.linspace(t_span[0], t_span[1], n)
    h = (t_span[1] - t_span[0]) / (n-1)
    print("h = ", h)
    Y_values = np.zeros((n, len(y0)))
    Y_values[0] = y0
    
    for i in range(1, n):
        Y_values[i] = rk4_step(f, t_values[i-1], Y_values[i-1], h, c1, c2)
    
    return t_values, Y_values

t_rk4, sol_rk4 = solve_rk4(bubble_dynamics, t_span, y0, c1, c2, len(t_eval))
#unusedT, epSsol_rk4 = solve_rk4(bubble_dynamics, t_span, epsy0, c1, c2, len(t_eval))

err = -sol_rk4[:,0] + sol_rk45.y[0]
#print(min(err))
err = np.fabs(err)
h = 0

err2 = sol_rk45.y[0]-epsSol_rk45.y[0]
err2 = np.fabs(err2)


# Построение графиков
#plt.figure(figsize=(8, 5))
"""
axs[0].plot(t_rk4, sol_rk4[:, 0], label='RK4', color='orange',linestyle='solid')
axs[0].plot(sol_rk45.t, sol_rk45.y[0], label='RK45',color='red', linestyle='dashed')
axs[0].set_xlabel('t')
axs[0].set_ylabel('y(t)')
axs[0].set_title('Сравнение методов RK45 и RK4')
axs[0].legend()
axs[0].grid()


axs[3].plot(sol_rk45.t, epsSol_rk45.y[0], label='RK45', color='orange',linestyle='solid')
axs[3].set_xlabel('t')
axs[3].set_ylabel('y(t)')
axs[3].set_title('график решения с ошибкой eps = 5e-3 в начальных условиях')
axs[3].legend()
axs[3].grid()
"""

axs[0].plot(sol_rk45.t, sol_rk45.y[0], label='origY(t)',color='red', linestyle='solid')
axs[0].plot(sol_rk45.t, epsSol_rk45.y[0], label='errY(t)', color='blue',linestyle='dashed')
axs[0].set_xlabel('t')
axs[0].set_ylabel('y(t)')
axs[0].set_title('графики решения с ошибкой и без ошибок')
axs[0].legend()
axs[0].grid()

axs[1].plot(sol_rk45.t, err2, label='|Y(t) - epsY(t)|', color='orange',linestyle='solid')
axs[1].set_xlabel('t')
axs[1].set_ylabel('y(t)')
axs[1].set_title('график погрешности')
axs[1].legend()
axs[1].grid()
#plt.plot(t_rk4,err,label='|RK4 - RK45|',color='blue')

#plt.savefig('rk45Rk4.png',bbox_inches='tight')
plt.tight_layout()
plt.show()
