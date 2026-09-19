package model;
import java.util.Random;

public class Tabuleiro {
    private int[][] matriz = new int[10][10];
    private int[] palpites = new int[2];

    //construtor personalizado
    //criar o tabuleiro com valores aleatorios
    public Tabuleiro(){
        Random random = new Random();
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 10; j++) {
             matriz[i][j] = random.nextInt(0, 101); //geração de 0 a 100
            }
        }
    }

    public double jogar (int p1, int p2) {
        palpites[0] = p1;
        palpites[1] = p2;
        int totalAcertos = verificarAcertos();
        desenharResultado();
        if((totalAcertos) >= 3) {
            return 1000.0 * totalAcertos;
        } else {
            return 0;
        }
    }

    private void desenharResultado() {
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 10; j++) {
                if(matriz[i][j] == palpites[0] || matriz[i][j] == palpites[1]) {
                    System.out.printf("[%3d]*",matriz[i][j]);
                } else {
                    System.out.printf("[%3d] ",matriz[i][j]);
                }
            }
            System.out.println();
        }
    }

    private int verificarAcertos() {
        int total = 0;
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 10; j++) {
                if(matriz[i][j] == palpites[0] || matriz[i][j] == palpites[1]) {
                    total += 1;
                }
            }
        }
        return 0;
    }
}
