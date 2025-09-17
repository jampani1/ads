#include <stdio.h>

int main(void) {
    char nome[20];
    int idade, qtGols;
    printf("Digite seu nome: ");
    scanf("%s", &nome);
    printf("Digite sua idade: ");
    scanf("%d", &idade);
    printf("Digite a quantidade de gols marcados na sua carreira: ");
    scanf("%d", &qtGols);
    printf("Voce e o %s, tem %d anos e fez %d gols", nome, idade, qtGols);
    return 0;
}