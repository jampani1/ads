#include <stdio.h>

int main(void) {
    float compra;
    int tipoCliente;
    printf("Digite o valor da sua compra: \n");
    scanf("%f", &compra);
    printf("Digite o tipo do cliente: \n");
    scanf("%d", &tipoCliente);
    switch (tipoCliente) {
        case 1:
            printf("Preco final eh %.2f", compra); break;
        case 2:
            printf("Preco final com desconto de 5%% eh %.2f \n", compra*0.95);
            compra *= 0.95; break;
        case 3:
            printf("Preco final com desconto de 10%% eh %.2f \n", compra*0.9);
            compra *= 0.90; break;
        case 4:
            printf("Preco final com desconto de 15%% eh %.2f \n", compra*0.85);
            compra *= 0.85; break;
        default:
            printf("tipo inexistente"); return 1;
    }
    if (compra >= 500) {
        compra *= 0.95;
        printf("Como sua compra eh ENORME, toma mais desconto. Preco final: %.2f",compra);
    }
    return 0;
}