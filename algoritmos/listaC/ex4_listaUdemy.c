#include <stdio.h>

int main(void) {
    int vit, emp, der, pontos;
    printf("Digite o numero de vitorias: ");
    scanf("%d", &vit);

    printf("\nDigite o numero de empates: ");
    scanf("%d", &emp);

    printf("\nDigite o numero de derrotas: ");
    scanf("%d", &der);

    pontos = (vit * 3) + (emp * 1);

    printf("Seu time tem %d pontos", pontos);
    return 0;
}