"""
01_eda.py — Etapa 1: Análise Exploratória de Dados
Atividade de IC: Capacity Planning com Regressão Linear Simples.

===============================================================================
NATUREZA DAS VARIÁVEIS (escrever antes de calcular qualquer coisa)
===============================================================================

    dia            -> quantitativa DISCRETA, escala INTERVALAR.
                      Zero arbitrário (o "dia 1" é quando o monitoramento ligou,
                      não a origem do tempo). Não é variável aleatória: é o
                      índice da série, escolhido, não medido.

    uso_disco_gb   -> quantitativa CONTÍNUA, escala DE RAZÃO.
                      Zero absoluto (0 GB = disco vazio de verdade), então
                      "200 GB é o dobro de 100 GB" é uma frase válida.

No modelo clássico  y = β₀ + β₁·x + ε , o x é tratado como FIXO, conhecido sem
erro. Toda a aleatoriedade está no ε. Consequência prática: média e desvio de
`dia` não descrevem o servidor — descrevem o formato do dataset. Mas não são
inúteis: x̄ e Sxx = Σ(xᵢ−x̄)² são geometria do desenho e aparecem nas fórmulas
das Etapas 2 e 4.

-------------------------------------------------------------------------------
MATEMÁTICA DA ETAPA — desvio padrão de uma sequência 1, 2, ..., n
-------------------------------------------------------------------------------

Como `dia` é determinística, o desvio padrão dela tem forma fechada. Partindo de:

    Σi  = n(n+1)/2                 -> média x̄ = (n+1)/2
    Σi² = n(n+1)(2n+1)/6

e usando  Var_pop = Σi²/n − x̄²  :

    # TODO(você): fazer a simplificação no papel, em dois passos de fatoração,
    # e escrever o resultado aqui. Deve chegar em (n² − 1)/12.
    #
    #   Var_pop(1..n) = ...........................
    #
    # RESPOSTA:
    #   Var_pop = (n+1)(2n+1)/6 − (n+1)²/4
    #           = (n+1) · [ (2n+1)/6 − (n+1)/4 ]          ← põe (n+1) em evidência
    #           = (n+1) · [ (4n+2 − 3n−3) / 12 ]          ← denominador comum 12
    #           = (n+1)(n−1) / 12  =  (n² − 1)/12         ← produto notável
    #
    # Atenção: pandas/numpy com ddof=1 usam o estimador AMOSTRAL (divide por
    # n−1). A fórmula acima é POPULACIONAL (divide por n). Fator: n/(n−1).

===============================================================================
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --- configuração -------------------------------------------------------------
AQUI = Path(__file__).parent
CSV = AQUI / "monitoramento_disco_10k_v2.csv"
FIGURAS = AQUI / "figuras"
FIGURAS.mkdir(exist_ok=True)

SEED = 42  # regra da trilha: exemplo replicável
rng = np.random.default_rng(SEED)


# ==============================================================================
# PARTE A — Carregar e conferir a integridade do dataset
# ==============================================================================
df = pd.read_csv(CSV)

# A1 — o dataset é o que o enunciado promete?
#
# ATRIBUTO vs. MÉTODO, a distinção que decide se leva parênteses:
#   .shape .columns .dtypes .values  -> ATRIBUTOS. Algo que o objeto JÁ É.
#                                       A informação está guardada, é só ler.
#                                       SEM parênteses.
#   .describe() .head() .isna() .sum() -> MÉTODOS. Algo que o objeto FAZ.
#                                       Precisa calcular. COM parênteses.
# `df.shape()` dá erro porque você pega a tupla e tenta chamá-la como função.

print("dimensões (linhas, colunas):", df.shape)   # tupla, ex.: (10000, 2)
print("colunas:", list(df.columns))
print("tipos:\n", df.dtypes, sep="")
print("\nfaltantes por coluna:\n", df.isna().sum(), sep="")

# `assert CONDIÇÃO, "mensagem"` = "se a condição for falsa, PARE tudo e me avise".
# Pra validação de dado é melhor que `if`: você não quer desviar o fluxo, quer
# abortar. Se o dado está errado, nenhuma conta depois dele vale.
assert df.shape == (10000, 2), f"esperava (10000, 2), veio {df.shape}"
assert list(df.columns) == ["dia", "uso_disco_gb"], f"colunas: {list(df.columns)}"

# .isna() devolve um DataFrame de True/False do mesmo tamanho.
# O primeiro .sum() soma por coluna (vira uma Series, um total por coluna);
# o segundo .sum() soma essa Series (vira um número só).
assert df.isna().sum().sum() == 0, "existe valor faltante no dataset"

# `dia` é mesmo 1, 2, 3, ..., n — sem buraco, sem repetição e em ordem?
# np.arange(1, n+1) gera [1, 2, ..., n]. O n+1 é porque o fim é EXCLUSIVO.
esperado = np.arange(1, len(df) + 1)
assert np.array_equal(df["dia"].values, esperado), "a coluna `dia` não é 1..n"

print("\n>>> PARTE A OK — dataset íntegro, x = 1..n confirmado.\n")


# ==============================================================================
# PARTE B — Estatísticas descritivas (item 1 do enunciado)
# ==============================================================================
# B1 — a tabela descritiva (referência trabalhada; leia os comentários).
#
# describe() devolve um DataFrame onde as LINHAS são as estatísticas
# (count, mean, std, min, 25%, 50%, 75%, max) e as COLUNAS são as colunas
# numéricas do df. Ou seja: é uma tabela, não um texto.
#
# .loc[[...]] seleciona linhas PELO RÓTULO (o nome da linha), não pela posição.
#   - colchete duplo: o de fora é o .loc, o de dentro é a LISTA de rótulos.
#   - a ordem da lista é a ordem em que as linhas saem. Você manda na tabela.
#   - se fosse por posição seria .iloc[[0, 1, 2]] — aqui rótulo é mais seguro,
#     porque não depende de describe() manter a mesma ordem.
descritivas = df.describe().loc[["mean", "std", "min", "50%", "max"]]

# Renomeia os rótulos pro português do relatório. index= são as linhas
# (columns= seriam as colunas). O dicionário é {nome_antigo: nome_novo}.
descritivas = descritivas.rename(
    index={
        "mean": "média",
        "std": "desvio padrão",
        "min": "mínimo",
        "50%": "mediana",
        "max": "máximo",
    }
)

print("=== Etapa 1.1 — estatísticas descritivas ===")
# .round(2) arredonda; .to_string() imprime a tabela inteira sem truncar.
print(descritivas.round(2).to_string(), "\n")

# TODO(B1b): essa tabela vai LITERAL pro relatório. Copie a saída pro
# RELATORIO.md como tabela markdown assim que ela estiver do seu gosto.
#
# RESPOSTA: vai para o README.md da pasta. Só a coluna `uso_disco_gb` é
# descrição do servidor; a de `dia` entra como verificação de integridade
# (os cinco valores dela saem de n, ver Checkpoint 1).

# TODO(B2) — CHECKPOINT 1: validar o desvio padrão de `dia` contra a fórmula.
#   1. n = len(df)
#   2. var_pop  = (n**2 - 1) / 12
#   3. var_amostral = var_pop * n / (n - 1)
#   4. compare np.sqrt(var_amostral) com df["dia"].std()
#   Use np.isclose() e imprima os dois números lado a lado.
#   Se bater: você entendeu a diferença entre desvio populacional e amostral —
#   a mesma ideia do n−2 que volta na Etapa 3.

n = len(df)
var_pop = (n**2 - 1) / 12
var_amostral = var_pop * n / (n - 1)

# Dar nome aos dois valores: calcula uma vez, usa três. (Era isso que os `a` e
# `b` do meu exemplo queriam dizer — nome de exemplo, não nome de verdade.)
desvio_formula = np.sqrt(var_amostral)
desvio_pandas = df["dia"].std()

print("=== Checkpoint 1 — desvio padrão de `dia` ===")
print(f"fórmula: {desvio_formula:.12f}")
print(f"pandas : {desvio_pandas:.12f}")
assert np.isclose(desvio_formula, desvio_pandas), (
    f"não bateu: {desvio_formula} vs {desvio_pandas}"
)
print(">>> CHECKPOINT 1 OK — o desvio de uma sequência 1..n é pura aritmética.\n")


# TODO(B3): leitura crítica de `uso_disco_gb`. Responda EM COMENTÁRIO aqui,
# com os números que saíram:
#   - média vs. mediana: próximas (simétrica) ou destoantes (assimetria/outlier)?
#   bem proximas, simétricas
#   - o mínimo: é plausível fisicamente? tem cara de piso artificial do gerador?
#   é plausivel, uso de 10gb em um dia parado (domingo?)
#   - o MÁXIMO comparado com 5000 GB (o limite da Etapa 4): guarde esse número,
#     ele volta no Checkpoint 7 e provavelmente vai te surpreender.
#   maximo deu 5109 gb, estourou muito o limite? como é possivel?
#   - ARMADILHA: o desvio padrão de `uso_disco_gb` NÃO é o ruído diário. Como
#     y tem tendência, esse desvio mistura "crescimento ao longo da série" com
#     "flutuação de um dia pro outro". Quem mede o ruído é o desvio dos
#     RESÍDUOS, que só existe depois da Etapa 2. Escreva isso com suas palavras:
#
#     # >>> nao entendi muito bem o que o desvio padrao representa, mas entendi que nao conseguimos medir "cru" porque os dias aumentam sucetivamente, o que gera um ruído na interpretação > como tem tendencia geral de aumentar, tendencia de um dia pro outro eh diferente? nao entendi mesmo
#
#     # >>> TODO(B3b): reescrever a resposta acima com a ideia de "em torno de quê?".
#     #     Desvio padrão = distância típica dos pontos até uma REFERÊNCIA.
#     #     Com ȳ (linha HORIZONTAL) -> mede sobretudo a INCLINAÇÃO da nuvem.
#     #     Com ŷᵢ (linha INCLINADA) -> mede a ESPESSURA da faixa = o ruído diário.
#     #     Mesma fórmula, referência diferente. É o SST vs. SSE da Etapa 3.
#
# RESPOSTA (revisada):
#   - média 2370,83 × mediana 2361,63: diferença de 0,4% → distribuição simétrica.
#     (Simétrica porque y sobe de forma uniforme ao longo de dias igualmente
#     espaçados — é a forma da RETA, não a forma do ruído.)
#   - mínimo 10,00 GB: plausível como número, mas NÃO como dado natural — ver B4:
#     101 dias exatamente iguais a 10,00 é piso artificial (censura), não domingo.
#   - máximo 5109,21 GB: já passou do limite de 5000 GB. Não é contradição: a
#     reta (média) ainda não chegou lá, quem passou foi o ruído para cima (B4a).
#   - desvio padrão 1314,90 GB: é a distância típica até ȳ = 2370 GB, uma linha
#     HORIZONTAL. Como o disco vai de ~130 a ~4600 GB, quase todo esse desvio
#     é a subida ao longo dos 10.000 dias, não a oscilação de um dia. Medido em
#     torno da RETA (Etapa 3), o desvio cai para ~228 GB: essa é a espessura da
#     faixa, o ruído de verdade. Mesma fórmula, outra referência.


# ------------------------------------------------------------------------------
# B4 — investigação do mínimo e do máximo
# ------------------------------------------------------------------------------
# `idxmin()`/`idxmax()` devolvem o RÓTULO DA LINHA onde está o menor/maior valor
# (não o valor em si). O `.loc[]` então busca a linha inteira por esse rótulo —
# é assim que você descobre em QUE DIA o extremo aconteceu, não só quanto foi.
#
# Atenção ao tipo: `idxmin/idxmax` são métodos de Series (pandas). O `y` da
# Parte C é `.values`, um array NumPy, que NÃO os tem. Por isso a Series própria:
y_serie = df["uso_disco_gb"]

print("=== Investigação dos extremos ===")
print("linha do mínimo:\n", df.loc[y_serie.idxmin()], sep="")
print("\nlinha do máximo:\n", df.loc[y_serie.idxmax()], sep="")

# Piso artificial: um valor que se repete EXATAMENTE muitas vezes não é ruído.
n_no_piso = (y_serie == 10.0).sum()
print(f"\nlinhas com y exatamente == 10.00: {n_no_piso}")
print("faixa de dias em que isso ocorre:",
      df.loc[y_serie == 10.0, "dia"].min(), "a", df.loc[y_serie == 10.0, "dia"].max())

# Dias que já ultrapassaram o limite operacional de 5000 GB.
print(f"\ndias com y > 5000 GB: {(y_serie > 5000).sum()}")
print("primeiro deles:", df.loc[y_serie > 5000, "dia"].min(), "\n")

# RESULTADOS (rodado em 2026-09-25):
#
#   mínimo  -> dia 14, y = 10.00 GB
#   máximo  -> dia 9908, y = 5109.21 GB
#
#   y == 10.00 exatamente: 101 linhas, espalhadas do dia 14 ao dia 1102.
#   -> 101 repetições do MESMO valor não é coincidência: é PISO ARTIFICIAL.
#      O gerador fez y = tendência + ruído e cortou tudo abaixo de 10 GB,
#      porque nos primeiros dias a tendência ainda é pequena e o ruído puxaria
#      y para negativo — ocupação negativa não existe.
#      É a linha reta horizontal no canto inferior esquerdo dos painéis (a)/(b)
#      e a célula amarela isolada no (d). Nuvem de ruído não faz linha reta.
#      CONSEQUÊNCIA p/ Etapa 3: onde há corte, o resíduo não consegue ser tão
#      negativo quanto "gostaria" -> erros assimétricos naquela faixa, violando
#      uma hipótese do modelo. Isso vai aparecer no gráfico de resíduos.
#
#   y > 5000 GB: 9 dias, o primeiro no dia 9628 (todos no fim da série).
#   -> O disco JÁ ENCOSTOU no limite operacional dentro do período medido,
#      embora a tendência média ainda não tenha chegado lá. Quem estourou foi
#      o ruído para cima, não a reta.
#      TODO(B4a): escreva com suas palavras por que isso torna insuficiente a
#      resposta "o dia do estouro é onde a reta cruza 5000" da Etapa 4.
#
#      # >>> RESPOSTA: a reta é a ocupação MÉDIA esperada para cada dia. O disco
#      #     não estoura na média, estoura num dia concreto, com o ruído daquele
#      #     dia (±~228 GB). Se 9 dias já passaram de 5000 GB com a reta ainda
#      #     abaixo, o dia em que a reta cruza 5000 é tarde demais como resposta:
#      #     metade dos dias perto dali já estaria acima. A Etapa 4 troca a
#      #     pergunta por "quando o risco de um dia estourar fica relevante?".


# ==============================================================================
# PARTE C — Scatterplot e o problema do overplotting (item 2 do enunciado)
# ==============================================================================
# São 10.000 pontos. Plotados cru, a região densa vira mancha sólida e a
# informação de DENSIDADE se perde. Abaixo, quatro versões lado a lado: a
# ingênua (para mostrar o problema) e três correções, cada uma escondendo algo
# diferente. O painel (a) vai escrito como referência de idioma matplotlib —
# os outros três são seus.

x = df["dia"].values
y = df["uso_disco_gb"].values

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Ocupação do disco vs. dia — o problema do overplotting", fontsize=14)

# --- (a) ingênuo: tudo opaco, marcador grande -- REFERÊNCIA, já pronto --------
ax = axes[0, 0]
ax.scatter(x, y)  # sem s, sem alpha: cada ponto tampa o vizinho
ax.set_title("(a) scatter cru — 10.000 pontos opacos")
ax.set_xlabel("dia")
ax.set_ylabel("uso_disco_gb (GB)")

# --- (b) transparência + marcador pequeno -------------------------------------
# TODO(C1): mesmo scatter do painel (a), mas com:
#     s=...      tamanho do marcador, algo entre 1 e 5
#     alpha=...  transparência, algo entre 0.05 e 0.15
# O efeito: onde N pontos se sobrepõem, a opacidade acumula e a cor fica mais
# forte -> a sobreposição vira um GRADIENTE que você consegue ler.
# Experimente 3 valores de alpha antes de escolher. O que você perde: pontos
# isolados (outliers) ficam quase invisíveis.
ax = axes[0, 1]
ax.scatter(x, y, s=3, alpha=0.12)  # opacidade acumula onde há sobreposição
ax.set_title("(b) alpha baixo + marcador pequeno")
ax.set_xlabel("dia")
ax.set_ylabel("uso_disco_gb (GB)")

# --- (c) amostragem aleatória --------------------------------------------------
# TODO(C2): sortear 1.000 dos 10.000 índices, com seed fixa, e plotar só esses.
#     idx = rng.choice(len(df), size=1000, replace=False)
#     depois use x[idx] e y[idx]
# Note o `replace=False`: sem reposição, senão o mesmo dia pode sair duas vezes.
# O que você ganha: legibilidade, cada ponto visível. O que perde: a cauda —
# um evento raro tem ~10% de chance de entrar na amostra.
idx = rng.choice(len(df), size=1000, replace=False)
ax = axes[1, 0]
ax.scatter(x[idx], y[idx], s=10, alpha=0.7)
ax.set_title("(c) amostra aleatória de 1.000 pontos (seed fixa)")
ax.set_xlabel("dia")
ax.set_ylabel("uso_disco_gb (GB)")

# --- (d) densidade explícita ---------------------------------------------------
# TODO(C3): trocar o scatter por uma contagem por célula:
#     hb = ax.hexbin(x, y, gridsize=50, cmap="viridis", mincnt=1)
#     fig.colorbar(hb, ax=ax, label="pontos por célula")
# Aqui a densidade deixa de ser sugerida pela cor e passa a ser MEDIDA: a barra
# de cor tem unidade (nº de pontos). O que perde: o ponto individual não existe
# mais, só a célula. `mincnt=1` evita pintar célula vazia.
# Experimente gridsize=20 e gridsize=100 e veja o trade-off resolução x ruído.
ax = axes[1, 1]
hb = ax.hexbin(x, y, gridsize=50, cmap="viridis", mincnt=1)
fig.colorbar(hb, ax=ax, label="pontos por célula")
ax.set_title("(d) hexbin — densidade medida")
ax.set_xlabel("dia")
ax.set_ylabel("uso_disco_gb (GB)")

fig.tight_layout()
fig.savefig(FIGURAS / "01_overplotting_comparacao.png", dpi=150)

# TODO(C4): escolher UMA das quatro para o relatório e escrever aqui o porquê.
# Não existe resposta certa — existe justificativa. A pergunta que decide:
# "o que eu preciso que o leitor VEJA nesta figura?". Se é a tendência, uma
# escolha serve; se é o quanto o ruído é grande, outra.
#
#   # >>> escolhi (  ) porque ...
#acredito que o melhor seja o c com um ajuste nesse "lavado" - corrija para gerar o correto para o relatorio; quero esse para visualizar o tanto que aumentou por dia e como isso esta tendendo a atingir o limite, certo?
#
# RESPOSTA: certo — escolha (c). O "lavado" era o alpha=0.12 herdado do (b);
# com s=10 e alpha=0.7 cada ponto da amostra fica nítido. Para mostrar "como
# está tendendo a atingir o limite", a figura do relatório acrescenta a linha
# horizontal de 5000 GB. O preço da escolha, declarado: a amostra de 1.000
# esconde a cauda (dos 9 dias acima de 5000 GB, só ~1 entra, em média) — por
# isso esse número aparece no texto, não na figura.

fig_rel, ax = plt.subplots(figsize=(9, 5.5))
ax.scatter(x[idx], y[idx], s=10, alpha=0.7, label="amostra aleatória de 1.000 dias (seed 42)")
ax.axhline(5000, color="black", linestyle=":", linewidth=1.6, label="limite operacional (5.000 GB)")
ax.set_title("Ocupação do disco ao longo de 10.000 dias")
ax.set_xlabel("dia")
ax.set_ylabel("uso_disco_gb (GB)")
ax.legend(loc="lower right")
ax.grid(alpha=0.3)
fig_rel.tight_layout()
fig_rel.savefig(FIGURAS / "01_dispersao_relatorio.png", dpi=150)

plt.show()


# ==============================================================================
# PARTE D — Descrição do comportamento observado (item 3 do enunciado)
# ==============================================================================
# TODO(D1): responda EM COMENTÁRIO, olhando a figura. São três perguntas, não
# uma (a terceira está escondida no enunciado e é a que sustenta a Etapa 4):
#
#   1. A tendência é LINEAR (reta) ou CURVA (acelerando / desacelerando)?
#
#   2. Existe ruído em torno dela? De que ordem de grandeza, no olho, em GB?
#      (compare a "espessura" da faixa com a escala do eixo y)
#
#   3. O ruído é CONSTANTE ao longo do tempo, ou a faixa abre/fecha?
#      constante  -> homocedasticidade
#      abre/fecha -> heterocedasticidade
#      Aqui é só suspeita visual; a Etapa 3 mede isso no gráfico de resíduos.
#      Mas a resposta muda a recomendação final: se o ruído cresce, a incerteza
#      lá no futuro é MAIOR do que o RMSE médio faz parecer.
#
#   # >>> RESPOSTA:
#   1. LINEAR. A nuvem sobe como uma faixa reta do começo ao fim, sem acelerar
#      nem achatar. (A Etapa 3 confirma: polinômio de grau 2 não melhora nada.)
#   2. Há ruído, e grande em GB: a faixa tem uns ±450 GB de espessura no olho,
#      contra uma subida total de ~4500 GB. A Etapa 3 mede: s ≈ 228 GB.
#   3. CONSTANTE (homocedasticidade): a faixa tem a mesma espessura no início e
#      no fim. Conferência numérica com os resíduos da Etapa 2, por terço da
#      série: desvio 222 / 230 / 231 GB. O primeiro terço é um pouco menor por
#      causa do piso em 10 GB (a censura corta a parte de baixo da faixa).
#
# TODO(D2): antes de rodar o 02_ajuste.py, faça o CHECKPOINT 4 no papel (ou
# aqui mesmo): média de y dos primeiros ~500 dias, média dos últimos ~500 dias,
# divida a diferença pela distância em dias entre os centros dos dois blocos.
# Isso é uma reta de dois pontos — não é mínimos quadrados, mas tem que estar na
# MESMA ORDEM DE GRANDEZA do β̂₁ que vai sair na Etapa 2. Anote o valor aqui
# ANTES de calcular o ajuste, pra não ancorar no resultado:
#
#   # >>> estimativa grosseira de β₁ ≈ ........ GB/dia
#
# RESPOSTA: ≈ 0,4474 GB/dia (calculado abaixo). Primeiros 500 dias: média
# 253,4 GB, centro no dia 250,5; últimos 500: média 4503,8 GB, centro no dia
# 9750,5. (4503,8 − 253,4) / 9500 ≈ 0,447. O β̂₁ da Etapa 2 sai 0,4486 — razão
# 1,003. Mesma ordem de grandeza, como tinha que ser.

bloco_ini, bloco_fim = df.iloc[:500], df.iloc[-500:]
beta1_grosseiro = (
    (bloco_fim["uso_disco_gb"].mean() - bloco_ini["uso_disco_gb"].mean())
    / (bloco_fim["dia"].mean() - bloco_ini["dia"].mean())
)
print(f"=== Checkpoint 4 — estimativa grosseira de β₁ ≈ {beta1_grosseiro:.4f} GB/dia")
