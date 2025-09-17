/*
Verificação de Senha com Níveis de Acesso

Crie um programa que simule um sistema de login. Ele deve pedir ao usuário
um nome de usuário (string) e uma senha (string). Para simplificar, use senhas
pré-definidas. Se a senha for ”admin123”, o acesso é ”Administrador”. Se for
2
”user456”, o acesso é ”Usuário Padrão”. Qualquer outra senha é considerada
incorreta. Use if/else if para as verificações.
Entrada: Duas strings.
Saída: O nível de acesso ou uma mensagem de erro.
Exemplo:
Entrada: joao admin123
Saída: Bem-vindo, joao! Nível de acesso: Administrador.
*/

#include <stdio.h>
#include <string.h>

int main(void) {
    char user[20], password[20];
    printf("user: ");
    fgets(user, 20, stdin);
    user[strcspn(user, "\n")] = '\0';
    /* fazer assim para conseguir pegar o tamanho correto e evitar enviar um enter */
    printf("password: ");
    fgets(password, 20, stdin);
    password[strcspn(password, "\n")] = '\0';

    if (strcmp(password, "admin123") == 0) {
        printf("E ai, ADM %s ", user);
    } else if (strcmp(password, "user456") == 0) {
        printf("E ai, PADRAO %s ", user);
    } else {
        printf("=============================");
    }

    /* consideracao interessante nerd
     * strcmp vem de string compare
     * password == "adm123"
     * seria comparacao == entre duas strings (arrays de caracteres)
     * nao compara texto, compara endereco de memoria, e portanto, sempre sera F
     * strcmp retorna 0 quando sao exatamente iguais
     *                <1 quando a primeira str vier primeiro alfabeticamente
     *                >1 quando a segunda str vier primeiro alfabeticamente
     */

    return 0;
}
