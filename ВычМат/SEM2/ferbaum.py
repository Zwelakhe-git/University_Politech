import numpy as np
import matplotlib.pyplot as plt

def func(x,eps):
    return 4*eps * x*(1-x)

eps_range = np.linspace(0,1,101)
x_range = np.linspace(0,1,101)

#вичисляем разные значение при одном значении eps
result = [func(x_range,ep) for ep in eps_range]
result = np.array(result)

#вычисляем значения функции при одном значении x и разных значениях eps
result2 = [func(x,eps_range) for x in x_range]
result2 = np.array(result2)

values_for_single_epsilon = [result2[i,1] for i in range(len(x_range))]
fx = values_for_single_epsilon

Max = []
Max2 = []
fig,ax = plt.subplots(2,1,figsize=(15,7))
ax = ax.flat

for i in range(len(eps_range)):
        Max.append([eps_range[i],max(result[i])])
        ax[0].plot(eps_range[i]*np.ones_like(eps_range),result[i])

#x_range = [v for v in x_range]
#print(result2[x_range.index(0.5)])
maxIndex = fx.index(max(fx))


ax[1].plot(x_range,fx)
ax[1].scatter(x_range[maxIndex],fx[maxIndex],label=f"({x_range[maxIndex],fx[maxIndex]})")
ax[1].legend()
plt.show()
