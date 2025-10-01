#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(void) {
    char nota1[3], nota2[3], nota3[3], nota4[3];
    int n1, n2, n3, n4;
    float media;
    printf("Digite a primeira nota \n");
    scanf("%s", &nota1);
    if (strcmp(nota1, "A") == 0) {
        n1 = 10;
    } else if (strcmp(nota1, "B") == 0) {
        n1 = 8;
    } else if (strcmp(nota1, "C") == 0) {
        n1 = 6;
    } else if (strcmp(nota1, "D") == 0) {
        n1 = 4;
    } else if (strcmp(nota1, "F") == 0) {
        n1 = 0;
    } else {
        n1 = atof(nota1);
        if (n1 >= 0 && n1 <= 100) {
            if (n1 > 10) {
                n1 = n1 / 10;
            } else {
                n1 = n1;
            }
        }
    }

    printf("Digite a segunda nota \n");
    scanf("%s", &nota2);
    if (strcmp(nota2, "A") == 0) {
        n2 = 10;
    } else if (strcmp(nota2, "B") == 0) {
        n2 = 8;
    } else if (strcmp(nota2, "C") == 0) {
        n2 = 6;
    } else if (strcmp(nota2, "D") == 0) {
        n2 = 4;
    } else if (strcmp(nota2, "F") == 0) {
        n2 = 0;
    } else {
        n2 = atof(nota2);
        if (n2 >= 0 && n2 <= 100) {
            if (n2 > 10) {
                n2 = n2 / 10;
            } else {
                n2 = n2;
            }
        }
    }

    printf("Digite a terceira nota \n");
    scanf("%s", &nota3);
    if (strcmp(nota3, "A") == 0) {
        n3 = 10;
    } else if (strcmp(nota3, "B") == 0) {
        n3 = 8;
    } else if (strcmp(nota3, "C") == 0) {
        n3 = 6;
    } else if (strcmp(nota3, "D") == 0) {
        n3 = 4;
    } else if (strcmp(nota3, "F") == 0) {
        n3 = 0;
    } else {
        n3 = atof(nota3);
        if (n3 >= 0 && n3 <= 100) {
            if (n3 > 10) {
                n3 = n3 / 10;
            } else {
                n3 = n3;
            }
        }
    }

    printf("Digite a quarta nota \n");
    scanf("%s", &nota4);
    if (strcmp(nota4, "A") == 0) {
        n4 = 10;
    } else if (strcmp(nota4, "B") == 0) {
        n4 = 8;
    } else if (strcmp(nota4, "C") == 0) {
        n4 = 6;
    } else if (strcmp(nota4, "D") == 0) {
        n4 = 4;
    } else if (strcmp(nota4, "F") == 0) {
        n4 = 0;
    } else {
        n4 = atof(nota4);
        if (n4 >= 0 && n4 <= 100) {
            if (n4 > 10) {
                n4 = n4 / 10;
            } else {
                n4 = n4;
            }
        }
    }

    printf("As notas sao %d %d %d %d \n", n1, n2, n3, n4);
    media = ((n1*2)+(n2*2)+(n3*3)+(n4*3)) / 10.0;
    printf("E a media ponderada, considerando os pesos 2, 2, 3, 3, e igual a %.2f \n", media);
    printf("O conceito final do aluno e: ");
    if (media <= 2.9) {
        printf("F - reprovado \n");
    } else if (media <= 4.9) {
        printf("D - insuficiente \n");
    } else if (media <= 6.9) {
        printf("C - regular \n");
    } else if (media <= 8.9) {
        printf("B - bom \n");
    } else {
        printf("A - excelente \n");
    }

    if (media < 5) {
        printf("O aluno precisara de recuperacao... e para passar precisa de no minimo: %.2f \n", 10 - media);
    }

    return 0;
}