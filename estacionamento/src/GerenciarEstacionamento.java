import model.Carro;
import model.Pessoa;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class GerenciarEstacionamento {

    private List<Pessoa> clientes = new ArrayList<>();
    private Scanner sc = new Scanner(System.in); // esta fora do main, entao para chamar no main precisa de ge.sc
    public static void main(String[] args)  {
        GerenciarEstacionamento ge = new GerenciarEstacionamento();
        int opcao = 0;
        do {
            System.out.println("Gerenciar estacionamento Mulas & Veiculos");
            System.out.println("1. Cad Cliente");
            System.out.println("2. Cad Veiculo");
            System.out.println("3. Listar Cliente e Veiculo");
            System.out.println("4. Total de Veiculos por Cliente");
            System.out.println("5. Total geral de Veiculos");
            System.out.println("6. Total de Clientes");
            System.out.println("9. Sair");
            opcao = Integer.parseInt(ge.sc.nextLine());
            switch (opcao) {
                case 1 -> ge.execCadCliente(); 
                case 2 -> ge.execCadVeiculo();
                case 3 -> ge.execExibirClientesVeiculos();
                case 4 -> ge.execTotalVeiculosPorCliente();
                case 5 -> ge.execTotalGeralVeiculos();
                case 6 -> ge.execTotalClientes();
                case 9 -> System.out.println("Fim do programa");
                default -> System.out.println("Opcao inválida");
            }

        } while (opcao != 9);
    }
    private void execTotalClientes() {
        System.out.println("Total de Clientes: " + clientes.size());
    }

    private void execTotalGeralVeiculos() {
        int total = 0;
        for(Pessoa pessoa : clientes){
            total += pessoa.getCarros().size();
        }
        System.out.println("Total de Veiculos cadastrados: " + total);
    }

    private void execTotalVeiculosPorCliente() {
        //varrer a lista e mostrar o total de carros (tamanho da lista)
        for(Pessoa pessoa : clientes){
            System.out.println("Total de veiculos de " +
                    pessoa.getNome() + " =" + pessoa.getCarros().size());
        }
    }

    private void execExibirClientesVeiculos() {
        //varrer a lista e mostrar os dados
        for(Pessoa pessoa : clientes){
            pessoa.imprimir();
        }
    }

    private void execCadVeiculo() {
        System.out.println("Clientes atuais...");
        System.out.println("ID   | Nome ");
        int pos = 1;
        for(Pessoa pessoa : clientes){
            System.out.printf("%4d | %-50s\n", pos, pessoa.getNome());
            pos++;
        }
        System.out.println("Escolha o ID da pessoa a cadastrar o veiculo");
        pos = Integer.parseInt(sc.nextLine());
        pos--;
        Carro carro = new Carro();
        System.out.println("Digite o modelo do carro: ");
        carro.setModelo(sc.nextLine());
        System.out.println("Digite a placa do carro: ");
        carro.setPlaca(sc.nextLine());
        System.out.println("Digite ano de fabricacao: ");
        carro.setAno(Integer.parseInt(sc.nextLine()));
        System.out.println("Digite o valor do carro: ");
        carro.setValor(Double.parseDouble(sc.nextLine()));
        clientes.get(pos).adicionarCarro(carro);
        System.out.println("Carro: " + carro.getModelo() + " adicionado ao ");
        System.out.println("Cliente: " + clientes.get(pos).getNome());
    }

    private void execCadCliente() {
        Pessoa pessoa = new Pessoa();
        System.out.println("Digite o nome da pessoa: ");
        pessoa.setNome(sc.nextLine());
        System.out.println("Digite o email  da pessoa: ");
        pessoa.setEmail(sc.nextLine());
        System.out.println("Digite o telefone da pessoa: ");
        pessoa.setTelefone(sc.nextLine());
        System.out.println("Digite dia do nascimento: ");
        int dia = Integer.parseInt(sc.nextLine());
        System.out.println("Digite mes do nascimento: ");
        int mes = Integer.parseInt(sc.nextLine());
        System.out.println("Digite ano do nascimento: ");
        int ano = Integer.parseInt(sc.nextLine());
        pessoa.setDataNasc(LocalDate.of(ano, mes, dia));
        clientes.add(pessoa); //Pessoa adicionada como cliente
        System.out.println("Dados cadastrados com sucesso");
    }
}