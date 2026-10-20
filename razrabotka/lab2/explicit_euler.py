"""Явный метод Эйлера для задания 2, вариант C2."""
import argparse
import numpy as np
import matplotlib.pyplot as plt
from common import test_parameters, test2_parameters, teacher_parameters, spatial_rhs, error_metrics

def solve(N=40, dt=None, use_test=True, test_id=1):
    p = (test_parameters() if test_id == 1 else test2_parameters()) if use_test else teacher_parameters()
    R, T = p["R"], p["T"]
    h = R/N
    # Для постоянного k оценка диффузионного ограничения порядка h^2/(4*k).
    # Для общих коэффициентов это только ориентир; используем консервативную оценку.
    kvals = np.array([float(np.max(np.asarray(p["k"](np.array([x]), 0.0))))
                      for x in np.linspace(0, R, N+1)])
    kmax = float(np.max(kvals))
    dt_stab = h*h/(4.0*kmax) if kmax > 0 else np.inf
    if dt is None:
        dt = 0.8*dt_stab
    if dt > dt_stab:
        print(f"ВНИМАНИЕ: dt={dt:.4e} превышает ориентировочную оценку {dt_stab:.4e}.")
    nt = int(np.ceil(T/dt))
    t = np.linspace(0.0, T, nt+1)
    dt = t[1]-t[0]
    r = np.linspace(0.0, R, N+1)
    U = np.zeros((N+1, nt+1))
    U[:, 0] = p["phi"](r)
    for n in range(nt):
        U[:, n+1] = U[:, n] + dt*spatial_rhs(r, t[n], U[:, n], p)
    maxerr, rmserr = error_metrics(U, r, t, p["exact"])
    return p, r, t, U, dt_stab, maxerr, rmserr

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=40, help="число пространственных интервалов")
    ap.add_argument("--dt", type=float, default=None, help="шаг времени; по умолчанию 0.8 от оценки устойчивости")
    ap.add_argument("--teacher", action="store_true", help="использовать заготовку задачи преподавателя")
    ap.add_argument("--test", type=int, choices=[1, 2], default=1, help="номер теста с точным решением (1 или 2)")
    args = ap.parse_args()
    p, r, t, U, dt_stab, maxerr, rmserr = solve(args.N, args.dt, not args.teacher, args.test)
    print(p["name"])
    print(f"N={args.N}, h={r[1]-r[0]:.6g}, dt={t[1]-t[0]:.6g}")
    print(f"Ориентировочная оценка устойчивости dt <= {dt_stab:.6g}")
    if maxerr is not None:
        print(f"Максимальная ошибка: {maxerr:.6e}")
        print(f"Среднеквадратичная ошибка: {rmserr:.6e}")
    fig, ax = plt.subplots()
    for idx in np.linspace(0, len(t)-1, 5, dtype=int):
        ax.plot(r, U[:, idx], label=f"t={t[idx]:.3f}")
    ax.set(xlabel="r", ylabel="u(r,t)", title="Явный метод Эйлера — температура в цилиндре")
    ax.grid(True); ax.legend(); fig.tight_layout()
    fig.savefig("explicit_temperature.png", dpi=160)
    if p["exact"] is not None:
        fig, ax = plt.subplots()
        ax.plot(r, U[:, -1], "o-", label="численное")
        ax.plot(r, p["exact"](r, t[-1]), "--", label="точное")
        ax.set(xlabel="r", ylabel="u(r,T)", title="Сравнение при конечном времени")
        ax.grid(True); ax.legend(); fig.tight_layout()
        fig.savefig("explicit_comparison.png", dpi=160)
    plt.show()

if __name__ == "__main__":
    main()
