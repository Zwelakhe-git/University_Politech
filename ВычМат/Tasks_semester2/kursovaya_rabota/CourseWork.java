import library.RKF45;
import library.exception.RKF45Exception;
import library.FuncInterf;

import java.lang.Math;



public class CourseWork{
    public static void main(String[] args){
        //параметры для Quanc8
        FuncInterf mainfunc;
        double A = 0;
        double B = Math.PI / 2;
        double c2 = 1.00;

        //параметры для rkf45
        int N = 2;
        int nfe = 0;
        int maxnfe = 3000;
        int iflag = 1;
        double h = 0.075;
        double tBeg = 0, tEnd = 1;
        double RKrelerr = 0.0001, RKabserr = 0.0001;


        double[] xVec = new double[2];
        double[] dxVec = new double[2];

        xVec[0] = 0;
        xVec[1] = 0.05;

        //вычисляем значение для c1

        double c1 = 0.999999727870315;

        mainfunc = (n,t,x,dx) -> {
            //final double c1;
            dx[0] = x[0];
            dx[1] = c1 * x[1]/Math.pow( (1 + Math.pow(x[1],2) ), 3) - c2 * x[0] ;
            return 0;
        };

        RKF45 rkf45 = new RKF45(mainfunc,N,xVec,dxVec,tBeg,tEnd,RKrelerr,RKabserr,h,nfe,maxnfe,iflag);

        try{
            rkf45.complete();
            //System.out.printf("x = [%e, %e]\n",xVec[0],xVec[1]);
        }catch(RKF45Exception e){
            e.printStackTrace();
        }

        
    }
}