import library.FuncInterf;
import library.RKF45;
import library.exception.RKF45Exception;

import java.lang.Math;
import java.util.ArrayList;

public class Task32025{
    public static void main(String[] args){
        FuncInterf func,func2;
        int N = 3;
        int nfe = 0;
        int maxnfe = 3000;
        int iflag = 1;
        double h = 0.075;
        double h_print = 0.075;
        double relerr = 0.0001, abserr = 0.0001;
        double A = 0, B = 1;
        double[] dxvec = new double[N];
        double[] xvec = new double[N];

        xvec[0] = 7;
        xvec[1] = 2;
        xvec[2] = 1;
    
        
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

        //doesnt belong to this lab
        func2 = (n,t, Y, dx) -> {
            if (n != Y.length || n != dx.length){
                return -1;
            }
            double y1 = Y[0],y2 = Y[1],y3 = Y[2];
            dx[0] = y1 + y2;
            dx[1] = -y1 + y2 - y3;
            dx[2] = 3 * y2 + y3;

        //return [dy1dt, dy2dt, dy3dt]
            return 0;
        };
        //func.f(N,A,xvec,dxvec);
        //public RKF45(FuncInterf funcInterf, int NEQN, double[] y, double[] YP, double t, double TOUT, double RELERR,
        //double ABSERR, double h, int NFE, int MAXNFE, int IFLAG)
        
        RKF45 rkf45 = new RKF45(func2,N,xvec,dxvec,A,B,relerr,abserr,h,nfe,maxnfe,iflag);

        ArrayList<String> dependencies = new ArrayList<>();
        dependencies.add("x(t)");
        dependencies.add("y(t)");
        dependencies.add("z(t)");

        try{
            rkf45.complete();
            ArrayList<double[]> sol = rkf45.getYValues();
            ArrayList<Double> solt = rkf45.getTVals();
            //System.out.println(solt.size());
            //System.out.println(sol.get(1).length);

            System.out.print("\nt: [ ");
            for(double t: solt){
                System.out.print(t + " ");
            }
            System.out.println("]");

            int j = 0;
            while(j < dependencies.size()){
                System.out.print("\n" + dependencies.get(j) + ": [ ");
                for(int i = 0; i < sol.get(j).length; ++i){
                    System.out.print(sol.get(j)[i] + " ");
                }
                System.out.println("]");
                ++j;
            }
            


            //System.out.printf("Solution: x = [%e , %e, %e]\n",xvec[0],xvec[1],xvec[2]);
        }catch(RKF45Exception e){
            e.printStackTrace();
        }

    }
}
