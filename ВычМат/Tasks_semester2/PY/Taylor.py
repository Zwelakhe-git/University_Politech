#from math import factorial


class Taylor():
    def __init__(self):
        self.absErr = 1.0e-70
        self.pi = 3.141592653589793
    
    def fabs(self,x):
        if x < 0:
            return -x
        return x

    def factorial(self,n):
        if n == 0: return 1
        return n * self.factorial(n-1)
    
    def EXP(self,x):
        sum = 0
        n=0
        
        while True:
            s = x**n / self.factorial(n)
            if self.fabs(s) < self.absErr:
                sum += s
                break
            sum += s
            n += 1
        
        return sum
    
    def COS(self,x):
        sum = 0
        n=0
        while True:
            s = ((-1)**n) * (x**(2*n))/self.factorial(2*n)
            if self.fabs(s) < self.absErr:
                sum += s
                break
            sum += s
            n += 1
        return sum
    
    def SIN(self,x):
        sum = 0
        n=0
        while True:
            s = ((-1)**n) * (x**(2*n+1))/self.factorial(2*n+1)
            if self.fabs(s) < self.absErr:
                sum += s
                break
            sum += s
            n += 1
        return sum
    
    def Binomial(self,x,pow):
        sum = 1
        n = 1
        while True:
            prod = 1
            for i in range(n):
                prod *= pow - i
            #print(prod)
            try:
                s = (prod)/self.factorial(n) * x**n
            except OverflowError as e:
                print(n)
                n -= 1
                s = (prod)/self.factorial(n) * x**n
                #print(s)
                sum += s
                return sum
            if self.fabs(s) < self.absErr:
                sum += s
                break
            sum += s
            n += 1
        return sum
    
    def diff(self,x,F,order):
        h=1e-7
        sum = 0
        for i in range(order+1):
            sum += (-1)**i * F(x+(order-i)*h)*self.factorial(order)/(self.factorial(i)*self.factorial(order-i))
        return sum/h**order
    

T1 = Taylor()
print(1-T1.EXP(-1e-7))
#print(T1.COS(0.6))
#print(T1.SIN(0.9))


m = 10
N = m+1

def Cheb(i,A,B):
    pass
    #return (A+B)/2 + (A-B)*(-T1.COS((2*i+1)/(2*(N-1)+2)*T1.pi))/2

#cells = [Cheb(i,0,3) for i in range(N)]
#print(cells)
