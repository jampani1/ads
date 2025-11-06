#include <stdio.h>

int main(void) {
    int nota, somadasnotas = 0, somadosalunos = 0;
    printf("Para interromper e contabilizar os dados, digite algum numero negativo\n");
    while (1) {
        printf("Digite a nota \n");
        scanf("%d", &nota);
        if (nota == -1) break;
        somadasnotas += nota;
        somadosalunos += 1;
    }
    printf("A nota media da sala eh de \n %d", somadasnotas/somadosalunos);
    return 0;
}
