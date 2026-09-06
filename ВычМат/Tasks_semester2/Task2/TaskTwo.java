import library.*;

public class TaskTwo{
    public static void main(String[] args){
        System.out.println("Задача №2");
        int N = 3;
        int NDIM = N*2;
        double cond = 1.0;
        int flag = 0;
        int[] PVT= new int[N];
        double[][] A;
        System.out.printf("\nN = %d\n\n",N);

        MakeMatrix M = new MakeMatrix(N);
        M.init();
        A = M.getMatrix();
        System.out.print("рабочая матрица A\n");
        M.show();
        System.out.printf("\n\n");

        
        Decomp dB = new Decomp(N,NDIM,A,cond,PVT,flag);
        dB.decomp();
        flag = dB.getFlag();
        
        for(double[] row: A){
            StringBuilder sb = new StringBuilder();
            for(double col: row){
                sb.append(col + ",");
            }
            sb.setCharAt(sb.length()-1, '\0');
            System.out.println(sb.toString());
        }
        //проверка работы разложения
        if(flag != 0){
            System.out.println("failed to decompose".toUpperCase());
            if(flag == 2){
                System.out.println("POSSIBLE PROBLEMS:\n1. a == null\n2. pivot == null\n3. n < 1\n4. ndim < n");
            }
            if(flag == 3){
                System.out.printf("POSSIBLE PROBLEMS:\npivot is too small\ncond = %e\n",dB.getCond());
            }
            if(flag == 1){
                System.out.println("POSSIBLE PROBLEMS:\nfailed to create WORK Matrix");
            }
            //M.show();
            System.exit(1);
        }

        System.out.println("COND " + dB.getCond());
        //нахождение обратной матрицы
        double[][] AI = new double[N][N];
        double[][] E = new double[N][N];
        makeSingular(AI, N);
        makeSingular(E, N);
        
        Solve SLV;
        for(int i = 0;i < N;++i){
            SLV = new Solve(N,NDIM,A,AI[i],PVT);
            SLV.solve();
        }
        M.transpose(AI,N);
        System.out.print("обратная матрица AI\n");
        M.show(AI);
        System.out.printf("\n\n");

        M.init();
        A = M.getMatrix();
        double[][]  Adup = new double[N][N];
        cpy(A,Adup,N);
        
        M.multiply(AI, Adup, N);
        M.subtract(E, N);
        System.out.print("R = A*AI - E\n");
        M.show();
        System.out.printf("\n\n");

        System.out.printf("norm(R) = %e\n",M.normR());
    }

    public static void makeSingular(double[][] e,int N){
        for(int i = 0;i < N;++i){
            for(int j = 0;j < N;++j){
                if(j == i){
                    e[i][j] = 1;
                }
                else{
                    e[i][j] = 0;
                }
            }
        }
    }
    
    public static void cpy(double[][] a,double[][] b,int N){
        for(int i = 0;i < N;++i){
            for(int j = 0;j < N;++j){
                b[i][j] = a[i][j];
            }
        }
    }
}