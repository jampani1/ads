#include <stdio.h>
int main(void) {
    int qtdGols = 0, npartidas = 0;
    float media;

    printf("Digite a quantidade de gols: ");
    scanf("%d", &qtdGols);

    printf("\nDigite a quantidade de partidas: ");
    scanf("%d", &npartidas);

    media = (float) qtdGols / (float) npartidas;

    printf("Sua media de gols por partida e de: %.2f", media);
    return 0;
}