#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main (void) {
    /* time(NULL):
     * Essa função, da biblioteca <time.h>, retorna o número total de segundos
     * que se passaram desde 1 de janeiro de 1970. Como esse número é diferente a cada segundo,
     * ele é uma excelente semente para garantir que nosso ponto de partida seja sempre diferente.
     *
     * tenta acertar o switch certo ai
    */

    srand(time(NULL));

    int numeroJogador = 0;
    int numeroAleatorio = (rand() % 5) + 1;

    printf("Digite um numero: ");
    scanf("%d", &numeroJogador);

    if (numeroJogador == numeroAleatorio) {
        printf("Parabens voce e demais\n");
    } else {
        printf("Voce errou o numero secretissimo era %d \n", numeroAleatorio);
        switch (numeroJogador) {
            case 1:
                printf("Voce foi de 1, mas a sorte nao te ajudou\n"); break;
            case 2:
                printf(" Seu chute foi 2, tente novamente\n"); break;
            case 3:
                printf("Mirou em 3, errou outra vez\n"); break;
            case 4:
                printf("4? Quase, mas o numero era outro\n"); break;
            case 5:
                printf("5 e sempre uma boa aposta, mas nao deu certo\n"); break;
            default:
                printf("O numero so pode ser de 1 a 5, ne\n"); break;
        }
    }
    return 0;
}