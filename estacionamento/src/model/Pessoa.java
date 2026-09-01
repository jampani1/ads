package model;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class Pessoa {
    private String nome;
    private String telefone;
    private String email;
    private LocalDate dataNasc;

    //Relacionamento 0 - N
    private List<Carro> carros = new ArrayList<>();

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getTelefone() {
        return telefone;
    }

    public void setTelefone(String telefone) {
        this.telefone = telefone;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public LocalDate getDataNasc() {
        return dataNasc;
    }

    public void setDataNasc(LocalDate dataNasc) {
        this.dataNasc = dataNasc;
    }

    public List<Carro> getCarros() {
        return carros;
    }

    //metodo para adicionar carro na lista desta pessoa
    public void adicionarCarro(Carro carro){
        carros.add(carro); //adicionar um carro na lista da pessoa.
    }

    //imprimir os dados da pessoa e seus respectivos carros
    public void imprimir(){
        System.out.println("Dados da pessoa e seus veiculos");
        System.out.println("-------------------------------");
        System.out.println("Nome: " + nome);
        System.out.println("Telefone: " + telefone);
        System.out.println("Email: " + email);
        if(carros.isEmpty()){
            System.out.println("Não possui veiculos");
        }else{
            System.out.println("Total de Carros: " + carros.size());
            for(Carro carro : carros){
                carro.imprimir();
            }
        }
        System.out.println("-------------------------------");
    }
}