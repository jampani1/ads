#include <stdio.h>

int main(void) {
    double peso = 0.0, altura = 0.0, imc = 0.0;

    printf("Digite seu peso (kg): ");
    if (scanf("%lf", &peso) != 1) {
        printf("Entrada inválida para o peso.\n");
        return 1;
    }

    printf("Digite sua altura (m): ");
    if (scanf("%lf", &altura) != 1) {
        printf("Entrada inválida para a altura.\n");
        return 1;
    }

    if (peso <= 0 || altura <= 0) {
        printf("\nErro: O peso e a altura devem ser valores positivos.\n");
        return 1;
    }
    imc = peso / (altura * altura);

    printf("\nSeu IMC é: %.2f\n", imc); // Mostra o valor calculado
    printf("Classificação: ");

    if (imc < 18.5) {
        printf("Abaixo do peso\n");
    } else if (imc < 25.0) {
        printf("Peso normal\n");
    } else if (imc < 30.0) {
        printf("Excesso de peso\n");
    } else if (imc < 35.0) {
        printf("Obesidade classe I\n");
    } else if (imc < 40.0) {
        printf("Obesidade classe II\n");
    } else {
        printf("Obesidade classe III\n");
    }

    return 0;
}