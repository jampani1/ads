package models;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class Comandante {
    private String nome;
    private String credencial;
    private String patente;
    private LocalDate dataComissionamento;
    private List<NaveEspacial> naves = new ArrayList<>();

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getCredencial() {
        return credencial;
    }

    public void setCredencial(String credencial) {
        this.credencial = credencial;
    }

    public String getPatente() {
        return patente;
    }

    public void setPatente(String patente) {
        this.patente = patente;
    }

    public LocalDate getDataComissionamento() {
        return dataComissionamento;
    }

    public void setDataComissionamento(LocalDate dataComissionamento) {
        this.dataComissionamento = dataComissionamento;
    }

    public List<NaveEspacial> getNaves() {
        return naves;
    }

    //adicionar nave na lista do comandante
    public void adicionarNave(NaveEspacial nave) {
        naves.add(nave);
    }

    public void imprimir() {
        System.out.println("-------DADOS-----");
        System.out.println("-----------------");
        System.out.println("Nome: " + nome);
        System.out.println("Credencial: " + credencial);
        System.out.println("Patente: " + patente);
        System.out.println("Data de comissionamento: " + dataComissionamento);
        System.out.println("-----------------");
        if (naves.isEmpty()) {
            System.out.println("Comandante sem naves");
        } else {
            System.out.println("Total de naves: " + naves.size());
            for (NaveEspacial nave : naves) {
                nave.imprimir();
            }
        }
        System.out.println("-----------------");
    }


    
}
