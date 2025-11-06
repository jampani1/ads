#include <stdio.h>

int main(void) {
    int n, stotal = 0, spar = 0, s100 = 0;
    for (int i = 0; i < 10; ++i) {
        printf("Digite um numero \n");
        scanf("%d", &n);
        stotal += n;
        if (n % 2 != 0) {
            continue;
        } else {
            spar += n;
        }
        if (n > 100) {
            s100 += n;
        } else {
            continue;
        }
    }
    printf("Soma total, soma dos pares e soma dos >100 respectivamente \n %d \n %d \n %d", stotal, spar, s100);
    return 0;
}
