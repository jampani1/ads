#include <stdio.h>

int main(void) {
    int idade, kid = 0, adolesc = 0, adul = 0, idos = 0;
    while (1) {
        printf("Digite uma idade \n");
        scanf("%d", &idade);
        if (idade < 0) break;
        if (idade <= 12) {
            printf("Criança!");
            kid += 1;
        } else if (idade <= 17) {
            printf("Adolescente");
            adolesc += 1;
        } else if (idade <= 59) {
            printf("Adulto");
            adul += 1;
        } else {
            printf("Idoso");
            idos += 1;
        }
    }
    printf("Total de %d %s", kid+adolesc+adul+idos, (kid+adolesc+adul+idos == 1) ? "pessoa" : "pessoas");
    return 0;
}
