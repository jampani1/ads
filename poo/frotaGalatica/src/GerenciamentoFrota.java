import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import models.Comandante;
import models.NaveEspacial;

public class GerenciamentoFrota {

    private List<Comandante> comandantes = new ArrayList<>();
    private Scanner sc = new Scanner(System.in);
    public static void main(String[] args) {
        GerenciamentoFrota gf = new GerenciamentoFrota();
        int opcao = 0;
        do{
            System.out.println("==== Gerenciar Frota de naves ====");
            System.out.println("1. Cadastrar Comandante");
            System.out.println("2. Designar nave a um comandante");
            System.out.println("3. Mostrar frota completa");
            System.out.println("4. Relatório: Naves por comandante");
            System.out.println("5. Total Geral de Naves na Aliança");
            System.out.println("6. Total de Comandantes");
            System.out.println("9. Sair");
            opcao = Integer.parseInt(gf.sc.nextLine());
            switch (opcao){
                case 1 -> gf.execCadCliente();
                case 2 -> gf.execCadVeiculo();
                case 3 -> gf.execExibirClientesVeiculos();
                case 4 -> gf.execTotalVeiculosPorCliente();
                case 5 -> gf.execTotalGeralVeiculos();
                case 6 -> gf.execTotalClientes();
                case 9 -> System.out.println("Fim do Programa");
                default -> System.out.println("Opcao invalida");
            }
        }while(opcao!=9);
    }
  

}
