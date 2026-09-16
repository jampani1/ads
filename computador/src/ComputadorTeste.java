public class ComputadorTeste {
    public static void main (String[] args) {
        Computador comp1 = new Computador();
        comp1.setMarca("Hp");
        comp1.setModelo("Velho");
        comp1.setNumeroSerie(1234L);
        comp1.setPreco(500.00);
        comp1.setCor("Prata");
        comp1.imprimir();
        System.out.println();
        comp1.calcularValor();
        comp1.imprimir();
        
    }
}
