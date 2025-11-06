#include <stdio.h>

int main(void) {
    int senhaCorreta = 1234, tentativa = 0, max = 3;
    for (int i = 0; i <= 3; i++) {
        printf("Digite a senha: \n");
        scanf("%d", &tentativa);
        if (tentativa == senhaCorreta) {
            printf("Parabuains");
            break;
        } else {
            printf("Senha incorreta, tentativas restantes %d \n", max);
            max -= 1;
            if (i == 3) {
                printf("Acesso BLOCKED \n");
            }
        }
    }
    return 0;
}
