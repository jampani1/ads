package models;

public class NaveEspacial {
    private String nome;
    private String classeNave;
    private int anoFab;
    private double poderdeFogo;

    public String getNome() {
        return nome;
    }
    public void setNome(String nome) {
        this.nome = nome;
    }
    public String getClasseNave() {
        return classeNave;
    }
    public void setClasseNave(String classeNave) {
        this.classeNave = classeNave;
    }
    public int getAnoFab() {
        return anoFab;
    }
    public void setAnoFab(int anoFab) {
        this.anoFab = anoFab;
    }
    public double getPoderdeFogo() {
        return poderdeFogo;
    }
    public void setPoderdeFogo(double poderdeFogo) {
        this.poderdeFogo = poderdeFogo;
    }

    public void imprimir() {
        System.out.println("-------DADOS-----");
        System.out.println("-----------------");
        System.out.println("Nome: " + nome);
        System.out.println("Classe: " + classeNave);
        System.out.println("Ano de fabricação: " + anoFab);
        System.out.println("Poder de fogo: " + poderdeFogo);
        System.out.println("-----------------");
    }

    
}
