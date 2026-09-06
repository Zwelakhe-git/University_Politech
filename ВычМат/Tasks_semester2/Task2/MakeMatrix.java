import java.lang.Math;

public class MakeMatrix{
    private final int N;
    
    private double[][] B;

    public MakeMatrix(int n){
        N = n;
        B = new double[N][N];
    }
    
    public void init(){
        for(int i=0;i<N;++i){
            for(int k=0;k<N;++k){
                if(k==i){
                    B[i][k] = 0.01/((N-i+k)*(i+1));
                }
                else if(i<k){
                    B[i][k] = 0;
                }
                else{
                    B[i][k]=i*(N-k);
                }
            }
        }
    }
    public void show(){
        for(int i=0;i<N;++i){
            for(int j=0;j<N;++j){
                //String formatt = String.format("\t\t",B[i][j]);
                System.out.printf("%e\t",B[i][j]);
            }
            System.out.println("");
        }
    }
    public void show(double[][] A){
        for(int i=0;i<N;++i){
            for(int j=0;j<N;++j){
                //String formatt = String.format("%.4f\t",A[i][j]);
                System.out.printf("%e\t",A[i][j]);
            }
            System.out.println("");
        }
    }
    
    double[][] getMatrix(){
        return B;
    }

    public int transpose(double[][] a,int N){
        double[][] temp = new double[N][N];
        for(int i = 0;i < N;++i){
            for(int j = 0;j < N;++j){
                temp[j][i] = a[i][j];
                                
            }
        }
        for(int i = 0;i < N;++i){
            for(int j = 0;j < N;++j){
                a[i][j] = temp[i][j];
                
            }
        }
        return 0;
    }
    public int multiply(double[][] a,double[][] b,int N){
            for(int i = 0;i < N;++i){
                for(int j = 0;j < N;++j){
                    B[i][j]=0;
                    for(int k=0;k<N;++k){
                        B[i][j] += a[i][k]*b[k][j];
                    }
                }
            }      
        return 0;
    }
    public int subtract(double[][] b,int N){
        for(int i = 0;i < N;++i){
            for(int j = 0;j < N;++j){
                B[i][j] -= b[i][j];
            }
        }      
        return 0;
    }
    public double normR(){
        double res = 0;
        for(int i = 0;i < N;++i){
            for(int j = 0;j < N;++j){
                res += Math.pow(B[i][j],2);
            }
        }
        res = Math.sqrt(res);
        return res;
    }
}