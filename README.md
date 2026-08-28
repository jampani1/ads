### Estudo de POO em Java com VS Code

aulas e materiais do maromao https://maromopoo.netlify.app/

### config

Instale o pacote oficial de ferramentas de Java diretamente no marketplace do VS Code: 

* **Extension Pack for Java** (Desenvolvido pela Microsoft)

### atalho sout v que só tem na outra IDE

Como o VS Code não traz nativamente o atalho soutv (comum no IntelliJ), adicione esta configuração para facilitar os prints de variáveis: 

1. Pressione Ctrl + Shift + P (no Windows) para abrir a barra de comandos.
2. Selecione **Preferences: Configure User Snippets** (Trechos de Código do Usuário).
3. Escolha a linguagem **java** (abre o arquivo java.json).
4. Cole o código abaixo logo abaixo da primeira chave {:

json

"Print Variable soutv": {
    "prefix": "soutv",
    "body": [
        "System.out.println(\"${1:variavel} = \" + ${1:variavel});"
    ],
    "description": "Printa o nome e o valor de uma variavel"
}

Agora, basta digitar soutv + Enter dentro de qualquer método para gerar a estrutura de print inteligente automaticamente. 

# para iniciar a aula
git clone https://github.com/jampani1/poo

# limpa as credenciais de login salvas no Windows pelo Git
usar esse - versao antiga que pegou no computador "protocol=https`nhost=github.com" | git credential-manager erase

esse aqui nao funcionou - versao mais atualizada 
git credential-manager reject https://github.com

# remove as configurações globais de login que possam ter sido criadas
git config --global --unset-all credential.helper
git config --system --unset-all credential.helper


para getters e setters automatico
