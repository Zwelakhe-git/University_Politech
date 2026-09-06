import library.FuncInterf;
import java.lang.Math;

public class TeskThreeB{
    public static void main(String[] args){
        FuncInterf func;
        double h = 0.025;//0.049, 0.0495, 0.034
        double h_print = 0.075;
        double next_print = 0.0;
        int N = 2;
        double[] xvec = new double[N];  //представление вектора z
        double[] dxvec = new double[N]; //представление вектора f(t,z)
        double tIn = 0.0;
        double tOut = 1.5;

        double[] rkf45Result = new double[N];
        rkf45Result[0] = -1.642129e-02;
        rkf45Result[1] = 3.411281e-02;
        double eps = 1.2e-7;

        xvec[0] = 2;
        xvec[1] = 0.5;

        System.out.println("HINT = " + h);
        func = (n,t, x, dx) -> {
            if (n != x.length || n != dx.length){
                return -1;
            }
            double y = -14 * x[0] + 13 * x[1] + Math.cos(1 + t);
            double y2 = 20 * x[0] - 30 * x[1] + Math.atan(1 + (t * t));
            dx[0] = y;
            dx[1] = y2;
            return 0;
        };
        
        double[] z_intermediate = new double[N]; //временный вектор, для хранения компонентов первого вычисления
        double[] F1 = new double[N];
        double P_coef;
        while(tIn <= tOut){
            func.f(N,tIn,xvec,F1);//первое вычисление f(t,z)
            P_coef = 2.0 * h / 3.0;
            for (int k = 0; k < N; ++k){
                z_intermediate[k] = xvec[k] + P_coef * F1[k];
            }

            P_coef = h / 4.0;

            func.f(N,tIn + h * (2.0 / 3.0),z_intermediate,dxvec);//второе вычисление f(t,z)
            for (int k = 0; k < N; ++k){
                xvec[k] = xvec[k] + P_coef * (F1[k] + 3 * dxvec[k]);
            }//окончательные компоненты текщей итерации
            

            
            if(tIn >= next_print){
                System.out.printf("t = %.3f, x = [%e , %e]\n",tIn,xvec[0],xvec[1]);
                next_print += h_print;
            }
            tIn += h;
            
        }
        System.out.printf("t = %.3f, x = [%e , %e]\n",tIn,xvec[0],xvec[1]);
        System.out.printf("вектор погрешности\t[%e , %e]\n",Math.abs(xvec[0] - rkf45Result[0]), Math.abs(xvec[1] - rkf45Result[1]));

        if(Math.abs(xvec[0] - rkf45Result[0]) <= eps || Math.abs(xvec[1] - rkf45Result[1]) <= eps){
            System.out.println("there is some satisfaction");
        }        
    }
}