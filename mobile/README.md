### Desenvolvimento Mobile
Repositório criado para armazenar os projetos, exercícios e atividades da disciplina de **Desenvolvimento Mobile**. 

### Tecnologias Utilizadas

* **Linguagem / Framework:** React Native
* **Ambiente de Desenvolvimento:** VS Code / expo.dev (Expo > Snaks)

**Aluno:** jampani1
**Instituição:** FATEC
**Semestre:** ago/2026



para limpar as credenciais do github no notebook da fatec: 
cmdkey /delete:LegacyGeneric:target=git:https://github.com

---

## [TEMPORÁRIO — apagar depois de testar/entregar] Rodar calculadoraIMC na FATEC

1. Se der erro de credencial do GitHub, limpar antes (comando acima).
2. Clonar (primeira vez) ou atualizar (se já existir a pasta):
   ```
   git clone https://github.com/jampani1/mobile.git
   cd mobile
   git pull
   ```
3. Entrar no projeto do exercício:
   ```
   cd projetos/calculadoraIMC
   ```
4. Instalar dependências:
   ```
   npm install
   ```
5. Rodar no Expo:
   ```
   npx expo start
   ```
6. Escanear o QR code com o app **Expo Go** no celular (ou apertar `w` pra abrir no navegador).
7. Testar: preencher peso (kg) e altura (m), apertar **CALCULAR IMC**, conferir se
   aparece o valor do IMC (2 casas decimais) e a classificação correta.
8. Tirar os prints pra entrega: (a) código-fonte de `App.js`, (b) tela do app
   rodando com um resultado calculado.

---

