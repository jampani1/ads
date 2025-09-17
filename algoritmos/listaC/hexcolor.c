#include <stdio.h>
#include <ctype.h>

int main (void) {
    char caracter;
    printf("Digite um caractere de cor (R, V, A, P):\n");
    scanf(" %c", &caracter);
    switch (toupper(caracter)) {
        case 'A': printf("O codiguin hex para Azul e #0000FF"); break;
        case 'R': printf("O codiguin hex para Vermelho e #FF0000"); break;
        case 'V': printf("O codiguin hex para Verde e #00FF00"); break;
        case 'P': printf("O codiguin hex para Preto e #000000"); break;
        default: printf("Digite um codiguin valido ne"); break;
    }
    return 0;
}