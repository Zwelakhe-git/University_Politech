import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from initsyalizatsyaMatristy import B

def SOE(t):
    pass

t = np.linspace(0, 2, 100)
xt = 1/2*np.exp(t) + 1/2*np.cos(t) + 1/2*np.sin(t)
yt = 1/2*np.exp(t) - 1/2*np.cos(t) + 1/2*np.sin(t)
zt = -np.cos(t) - np.sin(t)

def init():
    ax.set_xlim(-1.0, 2.5)
    ax.set_ylim(-1.0, 2.5)
    del xdata[:]
    del ydata[:]
    del zdata[:]
    del tdata[:]
    line.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    return line

def run(data):
    x,y,z,t = data
    xdata.append(x)
    ydata.append(y)
    zdata.append(z)
    tdata.append(t)
    ax.set_title(f"t: {t:.2f}, ymax: {max([x,y,z]):.2f}")
    ymin, ymax = ax.get_ylim()
    xmin, xmax = ax.get_xlim()
    if t > xmax:
        ax.set_xlim(xmin, 2*xmax)
    if max([x,y,z]) > ymax:
        ax.set_ylim(ymin, 2*ymax)
        ax.set_xlim(ymin, 2*ymax)
    
    ax.figure.canvas.draw()
    line.set_data(xdata,tdata)
    line2.set_data(ydata,tdata)
    line3.set_data(zdata,tdata)
    
    return line,

fig,ax = plt.subplots()
line, = ax.plot([],[],label='x(t)')
line2, = ax.plot([],[],label='y(t)')
line3, = ax.plot([],[],label='z(t)')
ax.legend()
ax.set_title("t: ")
xdata, ydata, zdata, tdata = [],[],[],[]

#ani = animation.FuncAnimation(fig,run,frames=zip(xt,yt,zt,t),init_func=init)

#plt.show()

print("t,x1,x2,x3")
for i in range(3):
    print("%.2e,%.4e,%.4e,%.4e"%(t[i],xt[i],yt[i],zt[i]))

