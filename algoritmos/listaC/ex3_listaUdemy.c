#include <stdio.h>

int main(void) {
    int tempo = 0, horas = 0, minutos = 0;
    printf("Digite o tempo jogado em minutos: ");
    scanf("%d", &tempo);
    if (tempo >= 60) {
        horas = tempo / 60;
        minutos = tempo % 60;
        printf("O tempo de jogo e de %d horas e %d minutos", horas, minutos);
    } else {
        printf("O tempo de jogo e de %d minutos.", tempo);
    }
    return 0;
}