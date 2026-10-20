"""Автоматические проверки для задания 2, вариант C2."""
import numpy as np
from common import thomas, test_parameters, test2_parameters, spatial_rhs
from explicit_euler import solve as solve_explicit
from implicit_euler import solve as solve_implicit


def test_thomas():
    # Матрица [[4,1,0],[1,4,1],[0,1,3]], решение [1,2,3].
    a = np.array([1.0, 1.0])
    b = np.array([4.0, 4.0, 3.0])
    c = np.array([1.0, 1.0])
    x_true = np.array([1.0, 2.0, 3.0])
    d = np.array([6.0, 12.0, 11.0])
    x = thomas(a, b, c, d)
    assert np.allclose(x, x_true, atol=1e-12), (x, x_true)


def test_exact_data():
    for params in (test_parameters(), test2_parameters()):
        r = np.linspace(0.0, params['R'], 11)
        t = np.array([0.0, 0.3, 1.0])
        U = params['exact'](r[:, None], t[None, :])
        assert np.allclose(U[:, 0], params['phi'](r))
        assert np.isclose(float(params['v'](0.0)),
                          float(np.asarray(params['exact'](np.array([1.0 + 1e-6]), 0.0)).reshape(-1)[0] - np.asarray(params['exact'](np.array([1.0 - 1e-6]), 0.0)).reshape(-1)[0]) / 2e-6,
                          rtol=1e-4)


def test_solvers():
    results = []
    for test_id in (1, 2):
        pe, re, te, Ue, stab, maxe, rmse = solve_explicit(N=20, dt=None, use_test=True, test_id=test_id)
        assert np.isfinite(maxe) and maxe < 0.02, (test_id, 'explicit', maxe)
        pi, ri, ti, Ui, maxi, rmsi = solve_implicit(N=20, dt=0.0005, use_test=True, test_id=test_id)
        assert np.isfinite(maxi) and maxi < 0.02, (test_id, 'implicit', maxi)
        results.append((test_id, maxe, maxi, stab, te[1]-te[0], ti[1]-ti[0]))
    return results


if __name__ == '__main__':
    test_thomas()
    test_exact_data()
    print('Метод прогонки: OK')
    print('Начальные и граничные данные тестов: OK')
    for row in test_solvers():
        test_id, err_e, err_i, stab, dt_e, dt_i = row
        print(f'Тест {test_id}: явный max_err={err_e:.6e}, dt={dt_e:.3e}, dt_stab≈{stab:.3e}; '
              f'неявный max_err={err_i:.6e}, dt={dt_i:.3e}')
    print('Все проверки пройдены.')
