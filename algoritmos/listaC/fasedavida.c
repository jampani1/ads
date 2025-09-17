#include <stdio.h>
int main(void) {
    int idade;
    printf("Digite a sua idade: ");
    scanf("%d", &idade);
    if (idade < 0) {
        printf("Idade negativa cara\n");
    } else if (idade <= 12) {
        printf("Crianca\n");
    } else if (idade <= 17) {
        printf("Adolescente\n");
    } else if (idade <= 59) {
        printf("Adulto\n");
    } else {
        printf("Idoso\n");
    }
    return 0;
}

/* faixa de valor w switch nao funcionam de jeito nenhum
case com operacao logica == > < etc tambem nao funciona */
