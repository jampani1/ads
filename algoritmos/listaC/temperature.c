#include <stdio.h>

int main(void) {
    /* variavel para unidade de medida, C = 1, K = 2, F = 3 */
    char u;
    int tipoUn;
    float temper;
    printf("Digite a unidade que voce ta querendo em um caracter");
    scanf("%c", &u);
    printf("Digite a temperatura que voce ta querendo mudar");
    scanf("%f", &temper);
    if (u == 'C') {
        printf("Sua unidade %c representa Celsius\n", u);
        tipoUn = 1;
    } else if (u == 'K') {
        printf("Sua unidade %c representa Kevin", u);
        tipoUn = 2;
    } else if (u == 'F') {
        printf("Sua unidade %c representa Fahrenheit", u);
        tipoUn = 3;
    }
    switch (tipoUn) {
        case 1:
            printf("impressionante mudou muito ne! olha em Kelvin %.2f K\n", temper+273.15);
            printf("e em farenhits entao! nossa! %.2f \n F", (temper*1.8) + 32); break;
        case 2:
            printf("olha como agora ta mais legal! em Celsius nao e melhor? %.2f C", temper-273.15);
            printf("em farenhits voce nem vai acreditar... %.2f F", (temper - 273.15) * 1.8 + 32); break;
        case 3:
            printf("impressionante como em Celsius e mais legal ne %.2f C", (temper-32)*(5/9));
            printf("e em Kelvin entao que loucura pra fazer... %.2f K", (temper-32)*(5/9)+(273.15)); break;
    }

    return 0;
}