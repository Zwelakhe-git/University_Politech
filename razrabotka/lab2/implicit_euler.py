"""Неявный метод Эйлера для задания 2, вариант C2."""
import argparse
import numpy as np
import matplotlib.pyplot as plt
from common import test_parameters, test2_parameters, teacher_parameters, thomas, error_metrics

def build_operator(r, t, p):
    """Строит матрицу L(t), для которой du/dt=L(t)u+s(t).
    Граничные потоки и источники входят в s.
    """
    R = p["R"]; N = len(r)-1; h = r[1]-r[0]
    k, q, f = p["k"], p["q"], p["f"]
    lower = np.zeros(N); diag = np.zeros(N+1); upper = np.zeros(N)
    s = np.zeros(N+1)

    k0h = float(np.asarray(k(np.array([h/2]), t)).reshape(-1)[0])
    q0 = float(np.asarray(q(np.array([0.0]), t)).reshape(-1)[0])
    f0 = float(np.asarray(f(np.array([0.0]), t)).reshape(-1)[0])
    diag[0] = -4*k0h/h**2 - q0
    upper[0] = 4*k0h/h**2
    s[0] = f0

    for i in range(1, N):
        rp=(i+0.5)*h; rm=(i-0.5)*h
        kp=float(np.asarray(k(np.array([rp]),t)).reshape(-1)[0])
        km=float(np.asarray(k(np.array([rm]),t)).reshape(-1)[0])
        qi=float(np.asarray(q(np.array([r[i]]),t)).reshape(-1)[0])
        fi=float(np.asarray(f(np.array([r[i]]),t)).reshape(-1)[0])
        lower[i-1] = rm*km/(r[i]*h**2)
        upper[i] = rp*kp/(r[i]*h**2)
        diag[i] = -(lower[i-1]+upper[i])-qi
        s[i] = fi

    rh=R-h/2
    kh=float(np.asarray(k(np.array([rh]),t)).reshape(-1)[0])
    qN=float(np.asarray(q(np.array([R]),t)).reshape(-1)[0])
    fN=float(np.asarray(f(np.array([R]),t)).reshape(-1)[0])
    mass=R*h/2-h**2/8
    lower[N-1] = rh*kh/(mass*h)
    diag[N] = -lower[N-1]-qN
    s[N] = (R*p["v"](t))/mass + fN
    return lower, diag, upper, s

def solve(N=40, dt=0.01, use_test=True, test_id=1):
    p = (test_parameters() if test_id == 1 else test2_parameters()) if use_test else teacher_parameters()
    R,T=p["R"],p["T"]
    nt=int(np.ceil(T/dt))
    t=np.linspace(0.0,T,nt+1); dt=t[1]-t[0]
    r=np.linspace(0.0,R,N+1)
    U=np.zeros((N+1,nt+1)); U[:,0]=p["phi"](r)
    for n in range(nt):
        lower, diag, upper, s = build_operator(r,t[n+1],p)
        # (I - dt*L) U^{n+1} = U^n + dt*s^{n+1}
        a=-dt*lower
        b=1.0-dt*diag
        c=-dt*upper
        rhs=U[:,n]+dt*s
        U[:,n+1]=thomas(a,b,c,rhs)
    maxerr,rmserr=error_metrics(U,r,t,p["exact"])
    return p,r,t,U,maxerr,rmserr

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--N",type=int,default=40)
    ap.add_argument("--dt",type=float,default=0.01)
    ap.add_argument("--teacher",action="store_true")
    ap.add_argument("--test", type=int, choices=[1, 2], default=1, help="номер теста с точным решением (1 или 2)")
    args=ap.parse_args()
    p,r,t,U,maxerr,rmserr=solve(args.N,args.dt,not args.teacher,args.test)
    print(p["name"])
    print(f"N={args.N}, h={r[1]-r[0]:.6g}, dt={t[1]-t[0]:.6g}")
    if maxerr is not None:
        print(f"Максимальная ошибка: {maxerr:.6e}")
        print(f"Среднеквадратичная ошибка: {rmserr:.6e}")
    fig,ax=plt.subplots()
    for idx in np.linspace(0,len(t)-1,5,dtype=int):
        ax.plot(r,U[:,idx],label=f"t={t[idx]:.3f}")
    ax.set(xlabel="r",ylabel="u(r,t)",title="Неявный метод Эйлера — температура в цилиндре")
    ax.grid(True); ax.legend(); fig.tight_layout()
    fig.savefig("implicit_temperature.png",dpi=160)
    if p["exact"] is not None:
        fig,ax=plt.subplots()
        ax.plot(r,U[:,-1],"o-",label="численное")
        ax.plot(r,p["exact"](r,t[-1]),"--",label="точное")
        ax.set(xlabel="r",ylabel="u(r,T)",title="Сравнение при конечном времени")
        ax.grid(True); ax.legend(); fig.tight_layout()
        fig.savefig("implicit_comparison.png",dpi=160)
    plt.show()

if __name__=="__main__":
    main()
