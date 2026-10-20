"""Общие функции для задания 2, вариант C2.
Цилиндрическая геометрия, ИИМ (метод баланса).
"""
import numpy as np

def test_parameters():
    """Тест с известным точным решением u(r,t)=exp(-t)*(1+r**2)."""
    return {
        "R": 1.0,
        "T": 1.0,
        "k": lambda r, t: np.ones_like(np.asarray(r, dtype=float)),
        "q": lambda r, t: np.zeros_like(np.asarray(r, dtype=float)),
        "f": lambda r, t: -(5.0 + np.asarray(r)**2) * np.exp(-t),
        "phi": lambda r: 1.0 + np.asarray(r)**2,
        "v": lambda t: 2.0 * np.exp(-t),
        "exact": lambda r, t: np.exp(-t) * (1.0 + np.asarray(r)**2),
        "name": "Тест: u(r,t)=exp(-t)*(1+r^2)",
    }


def test2_parameters():
    """Тест 2 с точным решением u(r,t)=exp(-t)*(1+r^4)."""
    return {
        "R": 1.0,
        "T": 1.0,
        "k": lambda r, t: np.ones_like(np.asarray(r, dtype=float)),
        "q": lambda r, t: np.zeros_like(np.asarray(r, dtype=float)),
        "f": lambda r, t: -np.exp(-t) * (1.0 + 16.0*np.asarray(r)**2 + np.asarray(r)**4),
        "phi": lambda r: 1.0 + np.asarray(r)**4,
        "v": lambda t: 4.0*np.exp(-t),
        "exact": lambda r, t: np.exp(-t)*(1.0 + np.asarray(r)**4),
        "name": "Тест 2: u(r,t)=exp(-t)*(1+r^4)",
    }

def teacher_parameters():
    """Заготовка для параметров преподавателя.
    Заменить значения/функции после получения исходных данных.
    """
    R = 1.0  # TODO: радиус цилиндра
    T = 1.0  # TODO: конечное время
    def k(r, t):
        return np.ones_like(np.asarray(r, dtype=float))  # TODO
    def q(r, t):
        return np.zeros_like(np.asarray(r, dtype=float))  # TODO
    def f(r, t):
        return np.zeros_like(np.asarray(r, dtype=float))  # TODO
    def phi(r):
        return np.zeros_like(np.asarray(r, dtype=float))  # TODO
    def v(t):
        return 0.0  # TODO: граничная функция варианта C2
    return {"R": R, "T": T, "k": k, "q": q, "f": f,
            "phi": phi, "v": v, "exact": None,
            "name": "Задача преподавателя"}

def thomas(a, b, c, d):
    """Метод прогонки для трёхдиагональной системы.
    a: нижняя диагональ (n-1), b: главная (n), c: верхняя (n-1), d: правая часть (n).
    """
    a = np.asarray(a, dtype=float).copy()
    b = np.asarray(b, dtype=float).copy()
    c = np.asarray(c, dtype=float).copy()
    d = np.asarray(d, dtype=float).copy()
    n = len(b)
    if n == 1:
        return d / b
    for i in range(1, n):
        if abs(b[i-1]) < 1e-14:
            raise ZeroDivisionError("Нулевой ведущий элемент в методе прогонки")
        m = a[i-1] / b[i-1]
        b[i] -= m * c[i-1]
        d[i] -= m * d[i-1]
    x = np.empty(n)
    x[-1] = d[-1] / b[-1]
    for i in range(n-2, -1, -1):
        x[i] = (d[i] - c[i] * x[i+1]) / b[i]
    return x

def spatial_rhs(r, t, u, p):
    """Правая часть полудискретной системы du/dt=F(t,u), выведенной ИИМ."""
    R = p["R"]
    N = len(r) - 1
    h = r[1] - r[0]
    k = p["k"]
    q = p["q"]
    f = p["f"]
    du = np.zeros_like(u, dtype=float)

    # Узел оси: баланс на [0, h/2]
    k_half = float(np.asarray(k(np.array([h/2]), t)).reshape(-1)[0])
    q0 = float(np.asarray(q(np.array([0.0]), t)).reshape(-1)[0])
    f0 = float(np.asarray(f(np.array([0.0]), t)).reshape(-1)[0])
    du[0] = 4.0 * k_half * (u[1] - u[0]) / h**2 - q0*u[0] + f0

    # Внутренние узлы
    for i in range(1, N):
        rp = (i + 0.5) * h
        rm = (i - 0.5) * h
        kp = float(np.asarray(k(np.array([rp]), t)).reshape(-1)[0])
        km = float(np.asarray(k(np.array([rm]), t)).reshape(-1)[0])
        qi = float(np.asarray(q(np.array([r[i]]), t)).reshape(-1)[0])
        fi = float(np.asarray(f(np.array([r[i]]), t)).reshape(-1)[0])
        du[i] = (
            rp*kp*(u[i+1]-u[i])/h
            - rm*km*(u[i]-u[i-1])/h
        ) / (r[i]*h) - qi*u[i] + fi

    # Внешняя граница: интегральный баланс на [R-h/2, R].
    # Для C2: -k*u_r=-v(t), поэтому k*u_r=v(t).
    rhalf = R - h/2
    kh = float(np.asarray(k(np.array([rhalf]), t)).reshape(-1)[0])
    qN = float(np.asarray(q(np.array([R]), t)).reshape(-1)[0])
    fN = float(np.asarray(f(np.array([R]), t)).reshape(-1)[0])
    mass = (R*h/2.0) - h**2/8.0
    du[N] = (
        R * p["v"](t) - rhalf*kh*(u[N]-u[N-1])/h
    ) / mass - qN*u[N] + fN
    return du

def make_grid(p, N, dt):
    r = np.linspace(0.0, p["R"], N+1)
    nt = int(np.ceil(p["T"] / dt))
    t = np.linspace(0.0, p["T"], nt+1)
    return r, t

def error_metrics(U, r, t, exact):
    if exact is None:
        return None, None
    rr = r[:, None]
    tt = t[None, :]
    E = U - exact(rr, tt)
    return float(np.max(np.abs(E))), float(np.sqrt(np.mean(E**2)))
