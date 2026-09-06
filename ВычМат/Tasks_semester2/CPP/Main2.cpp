#include <stdio.h>
#include <math.h>   // Для exp()
#include "cmathsrc/spline.c" // Подключаем spline.c (можно отдельно скомпилировать как библиотеку)

#define N 11  // Количество узлов (0 ≤ k ≤ 10)
#define M 50  // Количество точек для интерполяции

int main() {
    double x[N], y[N];   // Узлы интерполяции
    double b[N], c[N], d[N]; // Коэффициенты сплайна
    int iflag;           // Флаг ошибки
    int last = 0;        // Начальный индекс для seval()

    // 1. Заполняем массивы x и y значениями f(x) = 1 - exp(-x)
    for (int k = 0; k < N; k++) {
        x[k] = 0.3 * k;
        y[k] = 1.0 - exp(-x[k]);
    }

    // 2. Вычисляем коэффициенты сплайна
    spline(N, 0, 0, 0.0, 0.0, x, y, b, c, d, &iflag);
    if (iflag != 0) {
        printf("Ошибка в spline(): iflag = %d\n", iflag);
        return 1;
    }

    // 3. Интерполяция и вывод результатов
    printf(" x       |  f(x) (точное)  |  S(x) (сплайн)\n");
    printf("---------------------------------------------\n");

    for (int i = 0; i <= M; i++) {
        double u = 0.3 * 10 * i / M;  // Точки от 0 до 3 (равномерное разбиение)
        double f_exact = 1.0 - exp(-u);
        double f_spline = seval(N, u, x, y, b, c, d, &last);

        printf("%8.4f | %14.8f | %14.8f\n", u, f_exact, f_spline);
    }

    return 0;
}
