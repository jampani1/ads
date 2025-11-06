#include <stdio.h>

int main(void) {
    int anterior, atual, prox, n;
    printf("Digite o N \n");
    scanf("%d", &n);
    if (n == 0) {
        printf("Sequencia nula");
    } else if (n == 1) {
        printf("Primeiro e unico numero eh 0");
    }
    anterior = 0;
    atual = 1;
    for (int i = 0; i < n; ++i) {
        printf("%d", anterior);
        prox = anterior + atual;
        anterior = atual;
        atual = prox;
    }
    return 0;
}
