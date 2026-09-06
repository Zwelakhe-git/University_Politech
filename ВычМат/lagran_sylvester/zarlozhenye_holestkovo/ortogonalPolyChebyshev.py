import numpy as np
import matplotlib.pyplot as plt

def T(x, n):
    if n == 0:
        return 1
    elif n == 1:
        return x
    else:
        return 2 * x * T(x, n - 1) - T(x, n - 2)

x = 3
n = 4

xrange = np.linspace(-1, 1, 100)
yplot = T(xrange, n)
roots = np.array([np.cos((2*k + 1)*np.pi/(2*n)) for k in range(n)])
peaks = np.array([np.cos(k*np.pi / n) for k in range(n+1)])
ypeaks = T(peaks, n)
yroots = T(roots, n)

singularPolynom = yplot / 2 ** (n-1)

fig, ax = plt.subplots()
ax.plot(xrange, yplot, color='red',lw=1)
ax.plot(xrange, singularPolynom,color='orange',lw=1)
ax.scatter(roots, yroots, color='blue', label=f"roots\ncount={len(roots)}")
ax.scatter(peaks, ypeaks, color='green',label=f"peaks\ncount={len(peaks)}")
ax.scatter(peaks, ypeaks/2**(n-1))

ax.set_title(f"Ортогональный полином Чебышева\nn={n}")
ax.grid()
ax.legend()
plt.show()