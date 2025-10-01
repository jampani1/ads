#include <stdio.h>

int main(void) {
    float salario, ir;
    printf("Digite seu salario bruto mensal para calcular o imposto de renda: \n");
    scanf("%f", &salario);
    if (salario <= 1903.98) {
        printf("Que legal, ou nao, voce esta isento!");
    }
    else if (salario <= 2826.65) {
        printf("Voce nao esta isento e devera pagar 7,5%%! \n");
        ir = salario * 0.075;
        printf("O valor total a ser pago de imposto de renda sera de: %.2f \n", ir);
        printf("O seu salario liquido sera de: %.2f", salario - ir);
    }
    else if (salario <= 3751.05) {
        printf("Voce nao esta isento e devera pagar 15%%! \n");
        ir = salario * 0.15;
        printf("O valor total a ser pago de imposto de renda sera de: %.2f \n", ir);
        printf("O seu salario liquido sera de: %.2f", salario - ir);
    }
    else if (salario <= 4664.68) {
        printf("Voce nao esta isento e devera pagar 22,5%%! \n");
        ir = salario * 0.225;
        printf("O valor total a ser pago de imposto de renda sera de: %.2f \n", ir);
        printf("O seu salario liquido sera de: %.2f", salario - ir);
    }
    else {
        printf("Voce nao esta isento e devera pagar 27,5%%! \n");
        ir = salario * 0.275;
        printf("O valor total a ser pago de imposto de renda sera de: %.2f \n", ir);
        printf("O seu salario liquido sera de: %.2f", salario - ir);
    }
    return 0;
}