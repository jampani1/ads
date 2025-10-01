#include <stdio.h>
#include <string.h>

int main(void) {
    int idade, tempo_empregado, dependentes, score = 100;
    float renda_mensal;
    char historico_cred[50], estado_civil[15];
    printf("Ola \n Qual a sua idade? \n");
    scanf("%d", &idade);
    printf("Qual sua renda mensal? \n");
    scanf("%f", &renda_mensal);
    printf("Ha quanto tempo voce esta empregado? \n");
    scanf("%d", &tempo_empregado);
    printf("Qual seu historico de credito? \n");
    scanf("%s", &historico_cred);
    printf("Qual seu estado civil? \n");
    scanf("%s", &estado_civil);
    printf("Voce tem dependentes? \nSe sim, quantos? Se não, digite 0\n");
    scanf("%d", &dependentes);

    if (idade >= 18 && idade <= 25) {
        printf("Baixo score, -25 pts \n");
        score = score - 25;
    } else if (idade > 25 && idade <= 60) {
        printf("Score normal \n");
    } else {
        printf("Score reduzido, -50 pts \n");
        score = score - 50;
    }

    if (tempo_empregado < 1) {
        printf("Score muito penalizado, -50 pts \n");
        score = score - 50;
    } else if (tempo_empregado <= 5) {
        printf("Score normal \n");
    } else {
        printf("Score valorizado, +50 pts \n");
        score = score + 50;
    }

    if (strcmp(historico_cred, "Excelente") == 0) {
        printf("Score valorizado, +50 pts \n");
        score = score + 50;
    } else if (strcmp(historico_cred, "Bom") == 0) {
        printf("Score valorizado, +25 pts \n");
        score = score + 25;
    } else if (strcmp(historico_cred, "Regular") == 0) {
        printf("Score inalterado \n");
    } else if (strcmp(historico_cred, "Ruim") == 0) {
        printf("Score muito penalizado, -50 pts \n");
        score = score - 50;
    }

    if (strcmp(estado_civil, "Casado") == 0) {
        printf("Score valorizado, +10 pts \n");
        score = score + 10;
    } else {
        printf("Score inalterado \n");
    }

    if (dependentes == 0) {
        printf("Score inalterado \n");
    } else {
        printf("Score penalizado, -10 pts a cada dependente \n");
        score = score - (dependentes * 5);
    }

    if (renda_mensal <= 2000.00) {
        printf("Aprovação necessita de renda maior do que 2000.00 \n");
        return 0;
    } else if (renda_mensal <= 3000.00) {
        printf("Score penalizado \n");
        score = score - 10;
    } else if (renda_mensal <= 3500.00) {
        printf("Score inalterado \n");
    } else if (renda_mensal <= 4000.00) {
        printf("Score pouco valorizado \n");
        score = score + 10;
    } else if (renda_mensal <= 4500.00) {
        printf("Score valorizado \n");
        score = score + 20;
    } else {
        printf("Score muito valorizado \n");
        score = score + 50;
    }

    if (score >= 150 && renda_mensal >= 2000.00) {
        printf("Emprestimo aprovado \n");
    } else {
        printf("Emprestimo negado devido as diretrizes da instituicao. \n");
    }

    return 0;
}