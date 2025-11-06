#include <stdio.h>

int main(void) {
    int x, y, p = 0, i = 0;
    printf("Digite um número \n");
    scanf("%d", &x);
    while (x > 0) {
        y = x % 10;
        if (y % 2 == 0) {
            p += 1;
        } else {
            i += 1;
        }
        x = x / 10;
    }
    printf("A quantidade de numeros pares e: %d \n", p);
    printf("A quantidade de numeros impares e: %d \n", i);
    return 0;
}
