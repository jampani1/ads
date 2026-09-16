import model.Esfera;
import java.util.Scanner;

public class CalculoGeometrico {
    public static void main(String[] args) {
        Esfera esfera = new Esfera();
        Scanner sc = new Scanner (System.in);
        System.out.println("Digite o valor do raio: ");
        esfera.setRaio(Double.parseDouble(sc.nextLine()));

        System.out.println("Volume da esfera: ");
        System.out.println(esfera.calcularVolume());
    }
}
