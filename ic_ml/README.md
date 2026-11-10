# IC — Introdução aos Paradigmas de Machine Learning
## Professor Marcio Rodrigues Sabino
### Aluno Maurício Jampani de Souza

Iniciação Científica: estudo, implementação própria e avaliação de algoritmos clássicos
de Machine Learning. Em cada modelo, a matemática vem antes do `import`, a implementação
é feita à mão e conferida contra a biblioteca de referência, e os resultados são
explicados com gráficos.

## Modelos

| | Modelo | Estudo | Status |
|---|---|---|---|
| 1 | **Regressão Linear** | [Previsão de esgotamento de disco](regressao_linear/) | ✅ concluído |
| 2 | **Regressão Logística** | [Previsão de entrega no prazo](regressao_logistica/) | ✅ concluído |
| 3 | k-NN | — | |
| 4 | Árvore de Decisão | — | |
| 5 | Random Forest | — | |
| 6 | K-Means | — | |
| 7 | Apriori | — | |
| 8 | PCA | — | |
| 9 | Q-Learning | — | |
| 10 | Detecção de Anomalias | — | |

---

## Curiosidades — o que os dados mostraram e o enunciado não pedia

### Regressão Linear

![Extrapolação com intervalos de confiança e de predição](regressao_linear/figuras/04_extrapolacao_bandas.png)

> **📉 861 dias ou 26 dias?**
> Invertendo a reta, o disco atinge o limite de 5.000 GB em 861 dias. Mas a reta é a
> ocupação *média*, e o disco não estoura na média: estoura num dia concreto. O dia em
> que passa a haver 5% de chance de uma leitura estourar chega em **26 dias**. A mesma
> pergunta, duas respostas, uma ordem de grandeza de diferença. E 9 dias da amostra já
> tinham passado do limite.

> **🧱 Um piso escondido nos dados.**
> 101 dias valem *exatamente* 10,00 GB. Um valor contínuo não se repete 101 vezes por
> acaso: é um corte do gerador, que evitou ocupação negativa no início da série. No
> gráfico de resíduos ele aparece como uma reta descendente, porque ali $e = 10 - \hat y$.

> **🎯 R² = 0,97 e erro de 228 GB, ao mesmo tempo.**
> Não é contradição. O R² mede quanto da variação a reta explica; como o disco sobe
> 4.500 GB ao longo da série, os 3% que sobram ainda são ±228 GB por dia. "1 − R²" não é
> margem de erro.

> **🔢 Estatística que não precisa de dados.**
> O desvio padrão da coluna `dia` (2.886,8957) sai só da fórmula $\sqrt{(n^2-1)/12}$,
> sem olhar o arquivo, e bate nas 12 casas. É a prova de que `dia` é um índice, não uma
> medição.

> **👀 Parecia padrão, não era.**
> A média móvel dos resíduos faz ondas de até ±45 GB que parecem ciclos. Medindo:
> Durbin-Watson = 2,03, e a média móvel oscila 16,09 GB contra 16,10 GB esperados para
> ruído puro. Não há autocorrelação; só o número separou "parece" de "é".

> **🧮 Duas contas, o mesmo resultado até a 10ª casa.**
> As fórmulas $S_{xy}/S_{xx}$ e a forma matricial $C^TC\beta = C^Ty$ vista em aula dão a
> mesma reta. Na forma matricial, a matriz é 2×2 com 4 pontos ou com 10.000; mas o número
> de condição dela sobe de 72 para 130 milhões, e é por isso que bibliotecas evitam
> montar $C^TC$.

### Regressão Logística

![Acurácia em função do limiar](regressao_logistica/figuras/03_acuracia_por_limiar.png)

> **🪜 O limiar ótimo é mais estreito que a grade.**
> A acurácia é uma escada: só muda quando o limiar cruza a probabilidade de algum pedido. O
> degrau que maximiza a acurácia tem 0,0046 de largura, entre 0,5037 e 0,5082. Uma busca de
> 0,01 em 0,01 passa por cima dele e para em 35 acertos, em vez de 36.

> **🔢 O número do pedido acerta mais que o modelo.**
> Ordenando por `PED-001` a `PED-042`, o resultado vem em blocos (15 atrasos, 3 acertos,
> 4 atrasos, 20 acertos), e um corte no número do pedido acerta 39 de 42, contra 36 da
> antecedência. É um vazamento: carrega a resposta sem explicar nada, e por isso fica de fora.

> **📏 85,7% na amostra, 81% fora dela.**
> O limiar foi escolhido olhando os mesmos 42 pedidos em que foi avaliado. Refazendo tudo sem
> um pedido de cada vez (*leave-one-out*), o limiar otimizado acerta 34, exatamente o mesmo que o
> 0,5 padrão. O ganho de um pedido era ajuste à amostra.

> **🔁 A logística começa na reta.**
> Não há fórmula fechada; o ajuste é iterativo. Pelo método de Newton, cada passo resolve o
> sistema $C^TC\beta = C^Ty$ da regressão linear com pesos, e o primeiro passo é exatamente
> quatro vezes a reta de mínimos quadrados ajustada em $y - 1/2$.

> **⚠️ O padrão do scikit-learn não é o do livro.**
> `LogisticRegression()` aplica regularização sem avisar e devolve coeficientes diferentes da
> máxima verossimilhança. Para reproduzir a conta feita à mão, é preciso `C=np.inf`.

> **🎯 Um pedido move o coeficiente em 35%.**
> Um único atraso com 22,81 h de antecedência, para o qual o modelo dava 95% de chance de
> chegar no prazo, segura a inclinação. Sem ele, $\hat\beta_1$ vai de 0,261 para 0,354.
