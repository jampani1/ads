package model;

public class Carta {
    private Valor valor;
    private Naipe naipe;

    public Carta (Valor valor, Naipe naipe) {
        this.valor = valor;
        this.naipe = naipe;
    }

    @Override
    public String toString() {
        return valor + " de " + naipe;
    }

    public Naipe getNaipe() {
        return naipe;
    }

    public Valor getValor() {
        return valor;
    }
}
