import matplotlib.pyplot as plt
import numpy as np
from Taylor import Taylor as T


cells = []
Yk = [0.15+0.3*k for k in range(10)]

for k in range(11):
    cells.append(0.3*k)

#теперь это используем для аппроксимации функции
def w(x,c):
    res = 1
    for val in cells:
        if val == c: continue
        res *= (x-val)
    return res

def F(x):
    return 1 - T().EXP(-x)

print(T().diff(cells[1],F,3))

def Q(x,cells):
    sum = 0
    for cell in cells:
        sum += w(x,cell)/w(cell,cell) * F(cell)
    
    return sum

def Spline(N,X,F,B,C,D,Y):
    """ X - узлы таблицы
        F - значения в этих узлах
        B,C,D - коэффициентов сплайнов
        N - число точек в таблице
    """
    i = 0
    #C.append(0)
    while i < N-1:
        if i==N-2:
            #вычисляем коэффициенты для краевого сплайна
            #к примеру берем N=3, X=[x1,x2,x3]
            #i=0,1,2
            #S2(x3) = a2 + b2(X[2]-X[1]) +...=F[x3]
            i+=1
            continue
            v = X[i+1]-X[i]
            coeff = np.array([[v,v**2,v**3],[0,2,6*v],[0,2,0]])
            sol = np.array([F[i+1]-F[i],0,T().diff(X[i],Y,2)])
            BCD = np.linalg.solve(coeff,sol)
            B.append(BCD[0])
            C.append(BCD[1])
            D.append(BCD[2])
        
        
        else:
            v = X[i+1]-X[i]
            if i==0:
                i+=1
                continue
            else:
                coeff = np.array([[v,v**2,v**3],
                         [1,2*v,3*v**2],[0,2,6*v]])
                sol = np.array([F[i+1]-F[i],T().diff(X[i+1],Y,1),T().diff(X[i+1],Y,2)])
            BCD = np.linalg.solve(coeff,sol)

            B.append(BCD[0])
            C.append(BCD[1])
            D.append(BCD[2])
        #splineCells = []
        #вычислить узлы в данном промежутке
        #splineCells.append([Cheb(j,cells[i],cells[i+1],4) for j in range(N)])
        #print(f"({cells[i],cells[i+1]}),{splineCells}\n")
        
        i += 1
    #C[N-2]=0

def SEVAL(N,U,X,F,B,C,D):
    sum = 0
    for i in range(N-1):
        sum += F[i] + B[i]*(U-X[i])+C[i]*(U-X[i])**2+D[i]*(U-X[i])**3



#определение выражения для ортогональных полиномов Чебышева
def Cheb(i,A,B,N):
    return (B+A)/2 + (B-A)*(-T().COS((2*i+1)/(2*(N-1)+2)*T().pi))/2



#построение с равностоящих узлов
y_vals1 = [Q(x,cells) for x in Yk]
y_vals2 = [F(x) for x in Yk]

B=[]
C=[]
D=[]
Fvals=[F(x) for x in cells]
#Spline(len(cells),cells,Fvals,B,C,D,F)
#print(B,'\n\n',C,'\n\n',D)

#print(Fvals[0]+B[0]*(cells[1]-cells[0])+C[0]*(cells[1]-cells[0])**2+D[0]*(cells[1]-cells[0])**3,
#      Fvals[1])
plt.plot(Yk,y_vals2,color='blue',label='F(x)')
plt.plot(Yk,y_vals1,color='red',label='Q(x)')

#график со значениями полинома чебышева


plt.title("Графики для функции, полинома Лагранжа и Сплайнов")
plt.xlim(cells[0]-0.5,cells[-1]+0.5)
plt.ylim(y_vals1[0],y_vals1[-1])
plt.grid()
plt.legend()
#plt.show()