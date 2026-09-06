#include <iostream>
#include <cmath>
#include "cmathsrc/spline.c"
#include <fstream>
#include <stdio.h>
#include <iomanip>


/*
функция, аппроксимация которой ищется
*/
double F(double x){
    return 1 - exp(-x);
}

/*
полином W(x)=(x-x0)...(x-xN-1)
xk - узлы таблицы
*/
double w(double x,double cells[],double c)
/*
x - точка, где ищется значение
c - исключаемый узел
cells - массив узлов таблицы
*/
{
    double res = 1;
    for (int i = 0; i < sizeof(cells) ; i++){
        if (cells[i] == c){  continue;   }
        res *= (x-cells[i]);
    }
    return res;
}
double Q(double x,double cells[])
/*вычисляет аппроксимацию фукнции полиномом Лагранжа.
Q(x) = W1(x)/W1(x1)*F(x1) + ... + WN(x)/WN(xN)*F(xN)
*/
{
    double sum = 0;
    for (int i = 0;i < sizeof(cells); i++){

        sum += w(x,cells,cells[i])/w(cells[i],cells,cells[i]) * F(cells[i]);
    }
    return sum;
}
int main(){
    int N = 11, M = 51;
    int flag,lst = 0;
    double x[N];
    double y[N];
    double Yk[N-1];

    double inputs[M];
    double splineOutput[M];
    double FOutput[M];
    double LagranOutout[M];

    double B[N];
    double C[N];
    double D[N];

    for (int i = 0 ; i < M ; ++i){

        inputs[i] = 0.3 * 10 * i/M;
    }
    
    for (int i = 0;i < N; i++){
        if (i < 10){
            Yk[i]=0.15 + 0.3 * i;

            x[i]=0.3*i;

            y[i]=F(x[i]);
        }
        else{
            x[i]=0.3*i;

            y[i]=F(x[i]);
        }
    }
   
    spline(N,0,0,0,0,x,y,B,C,D,&flag);

    if(flag != 0){
        if(flag == 1){
            std::cout << "less than two data points; cannot interpolate\n";
        }
        else if(flag == 2){
            std::cout << "x[] are not in ascending order\n";
        }
        return 1;
    }

    
    for (int i = 0; i < M ; i++){
        //вычислить значения фукнции в промежутке [0,3]
        splineOutput[i] = seval(N,inputs[i],x,y,B,C,D,&lst);

        FOutput[i] = F(inputs[i]);

        LagranOutout[i] = Q(inputs[i],x);
    }
    std::cout << (" x       |  f(x) (точное)  |  S(x) (сплайн)|  L(x) (лагранж) |\n");
    std::cout << ("--------------------------------------------------------------\n");
    
    for (int i = 0; i < M; i++) {
        std::cout << std::setw(8) << inputs[i] << " | " << std::setw(14) << FOutput[i] << " | "
        << std::setw(14) << splineOutput[i] << " | " << std::setw(14) << LagranOutout[i] << " | "     << std::endl;
    }
    
    for (int i = 0; i < 10 ; i++){
        splineOutput[i] = seval(N,Yk[i],x,y,B,C,D,&lst);

        FOutput[i] = F(Yk[i]);

        LagranOutout[i] = Q(Yk[i],x);
    }
    
    std::cout << (" x       |  f(x) (точное)  |  S(x) (сплайн)|  L(x) (лагранж) | F(x)-L(x)     | F(x)-S(x)     |\n");
    std::cout << ("----------------------------------------------------------------------------------------------\n");

    for (int i = 0; i < 10; i++) {
        std::cout << std::setw(8) << Yk[i] << " | " << std::setw(14) << FOutput[i] << " | "
        << std::setw(14) << splineOutput[i] << " | " << std::setw(14) << LagranOutout[i] << " | "
        << std::setw(14) << FOutput[i]-LagranOutout[i] << " | "  << std::setw(14) << FOutput[i]-splineOutput[i]
        << std::endl;
    }
    return 0;
}
