package model;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;

public class Baralho {
    private List<Carta> cartas = new ArrayList<>();
    //construtor personalizado
    //para: construir um baralho com 52 cartas
    public Baralho () {
        for (Naipe naipe : Naipe.values()) {
            Carta carta = new Carta(valor, naipe);
            cartas.add(carta);
        }
    }

    //metodo embaralhar
    public void embaralhar() {
        Collections.shuffle(cartas);
    }

    //metodo mostrarBaralho
    public void mostrarBaralho() {
        for (Carta carta : cartas) {
            System.out.println(carta);
        }
    }

    //metodo maiorValorCarta
    public Carta cartaMaiorValor(Carta carta1, Carta carta2) {
        if(carta1.getValor() == carta2.getValor()){
            if(carta1.getNaipe().ordinal() > carta2.getValor().ordinal()) {
                return carta1;
            } else {
                return carta2;
            }
        } else {
            if(carta1.getValor().ordinal() > carta2.getValor().ordinal()) {
                return carta1;
            } else {
                return carta2;
            }
        }
    }
}
