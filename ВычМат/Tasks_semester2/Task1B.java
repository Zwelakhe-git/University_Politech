import java.lang.Math;

import library.Quanc8;
import java.util.function.Function;

public class Task1B{
    
    public static void main(String[] args){
        double A = 0,B=Math.PI/2;
        double abserr = 2.2e-16;
        double relerr = 2.2e-16;
        double m=-1;

        Function<Double,Double> func = x -> Math.pow(Math.abs(Math.sin(x)-0.6),m);

        Quanc8 sol = new Quanc8(func,A,B,abserr,relerr);
        sol.calculate();
        System.out.println(sol.toString());

        
        double end1;
        double start2;
        double[] xeps = new double[20];//0.000005
        xeps[0] = 1e-7;
        for(int i = 1; i < 20; ++i){
            xeps[i] = xeps[i - 1] + 0.000005;
        }

        
        
        Quanc8 half2;
        System.out.println("eps     |    [A : B]        |    Res   |     ERR     |   Flag   | RES1 + RES2");
        System.out.println("--------+-------------------+----------+-------------+----------+-------------");
        for(double eps: xeps){
            end1 = 0.6435 - eps;
            start2 = 0.6435 + eps;

            sol = new Quanc8(func, A, end1, abserr, relerr);
            half2 = new Quanc8(func, start2, B,abserr, relerr);

            sol.calculate();
            half2.calculate();
            System.out.printf("%e| %f:%f |%10f|%e | %f |   \n",eps,A,end1,sol.getRESULT(),sol.getERREST(),sol.getFLAG());
            System.out.printf("%e| %f:%f |%10f|%e | %f | %e\n",eps,start2,B,half2.getRESULT(),half2.getERREST(),half2.getFLAG(), sol.getRESULT() + half2.getRESULT());
            System.out.println("--------+-------------------+----------+-------------+----------+-------------");

        }
        
        
        //System.out.printf("xeps = %f [ %f: %f ] res = %f err = %f  flag = %f\n",xepsilon,A,end1,sol.getRESULT(),sol.getERREST(),sol.getFLAG());
        //System.out.printf("xeps = %f [ %f: %f ] res = %f err = %f  flag = %f\n",xepsilon,start2,B,half2.getRESULT(),half2.getERREST(),half2.getFLAG());
        
        //double res = sol.getRESULT() + half2.getRESULT();
        //System.out.println(res);
        //double x_ = B - sol.getFLAG()*(B-A);
    }
}
