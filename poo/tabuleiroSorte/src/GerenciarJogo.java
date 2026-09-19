import model.Tabuleiro;

import java.util.Scanner;

public class GerenciarJogo {
    public static void main (String[] args) {
        Scanner sc = new Scanner(System.in);
        int p1, p2;
        System.out.println("Digite o palpite 1 do jogo [0 a 100]");
        p1 = Integer.parseInt(sc.nextLine());
        System.out.println("Digite o palpite 2 do jogo [0 a 100]");
        p2 = Integer.parseInt(sc.nextLine());

        Tabuleiro tabuleiro = new Tabuleiro();
        double premio = tabuleiro.jogar(p1, p2);
        if(premio > 0.0) {
            System.out.println("Parabéns, ganhou R$ " + premio);
        } else {
            System.out.println("Infelizmente não foi dessa vez. . .");
        }
    }
}
