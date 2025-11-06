#include <stdio.h>

int main(void) {
    int n1, n2, opc;
    do {
        printf("Menu da calculadora: \n");
        printf("1. Soma \n");
        printf("2. Subtração \n");
        printf("3. Multiplicação \n");
        printf("4. Divisão \n");
        printf("0. Sair \n");
        printf("Escolha uma opção: \n");
        scanf("%d", &opc);
        if (opc == 0) break;
        printf("Digite o primeiro valor: \n");
        scanf("%d", &n1);
        printf("Digite o segundo valor: \n");
        scanf("%d", &n2);
        switch (opc) {
            case 1: printf("Soma de %d + %d = %d \n", n1, n2, n1+n2); break;
            case 2: printf("Subtração de %d - %d = %d \n", n1, n2, n1-n2); break;
            case 3: printf("Multiplicação de %d * %d = %d \n", n1, n2, n1*n2); break;
            case 4:
                if (n2 == 0) printf("Impossível dividir por 0! \n");
                else printf("Divisão de %d / %d = %d \n", n1, n2, n1/n2); break;
        }
    } while (1);
    printf("Fim do programa \n");
    return 0;
}
