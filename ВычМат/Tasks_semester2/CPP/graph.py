import matplotlib.pyplot as plt
import csv

#сначала нужно удалить запятые в конце каждой строке в файле x_vals.csv
filename = "x_vals.csv"
splineoutput = []
Foutput = []
LagranOut = []
inputs = []

with open(filename,'r') as f:
    reader = csv.reader(f)
    inputs = [float(x) for x in next(reader)]
    splineoutput = [float(x) for x in next(reader)]
    Foutput = [float(x) for x in next(reader)]
    LagranOut = [float(x) for x in next(reader)]

#print(LagranOut,'\n',splineoutput,'\n',Foutput)

plt.style.use('seaborn-v0_8')
plt.plot(inputs,Foutput,label="F(x)",color='blue')
plt.plot(inputs,LagranOut,label="L(x)",color='black')
plt.plot(inputs,splineoutput,label="S(x)",color='red')
#plt.scatter(1.64, Foutput[28], facecolor='white',edgecolor='black',zorder=5)
#plt.text(1.64, Foutput[28],'(1.5)', horizontalalignment='left',verticalalignment='bottom')

plt.title("Graphs for values of F(x), L(x), S(x)")
plt.xlabel('X')
plt.ylabel('Y')
plt.grid()
plt.legend()
plt.xlim(inputs[0]-0.1,inputs[-1]+0.1)
plt.ylim(Foutput[0]-0.15,Foutput[-1]+0.15)
plt.tick_params(axis='y',labelsize=14)
plt.show()
