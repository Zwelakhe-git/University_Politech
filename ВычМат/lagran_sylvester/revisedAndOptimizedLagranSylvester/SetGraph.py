import matplotlib.pyplot as plt


fig, ax = plt.subplots()
line, = ax.plot([],[], lw=1, label="x(t)")
line2, = ax.plot([],[], lw=1, label="y(t)")
line3, = ax.plot([],[], lw=1, label="z(t)")
ax.legend()
ax.set_title("t: ")
x1,x2,x3, tdata = [], [], [], []