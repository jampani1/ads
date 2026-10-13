"""
02_ajuste.py — Etapa 2: Ajuste do Modelo Estatístico
Atividade de IC: Capacity Planning com Regressão Linear Simples.

===============================================================================
COMO USAR ESTE ARQUIVO
===============================================================================

    1. Cada função abaixo tem CONTRATO (o que entra, o que sai, a definição
       matemática) e corpo vazio. O "o quê" está dado; o "como" é seu.
    2. Rode o arquivo. O bloco de VERIFICAÇÃO no fim roda sozinho e acusa
       quantas checagens passaram. Agora: 0/6.
    3. Meta: 6/6.

    ESTADO FINAL (12/10/2026): modo guia encerrado para este exercício. Funções
    implementadas, respostas abaixo de cada pergunta (marcadas RESPOSTA), e dois
    acréscimos: o Caminho 2 (forma matricial da folha do professor) e as
    verificações V7 e V8. Resultado: 8/8 (7/7 quando o sklearn está bloqueado).

    Nenhuma linha está pronta para copiar, e NENHUM teste contém a resposta
    numérica — todos são identidades matemáticas. Você consegue provar que está
    certo sem consultar gabarito nenhum.

    Travou? Bloco DICAS no fim do arquivo (conceito, não código). Se não
    resolver, pergunte.

===============================================================================
MATEMÁTICA DA ETAPA — mínimos quadrados (referência)
===============================================================================

Modelo:  ŷ = β₀ + β₁·x     (mesmo `a` e `b` do hoje1409/linreg.py, outra roupa)
pode explicar melhor sobre isso igual voce fez em uma resposta, dizendo sobre essa relação de a e o que significa
a simbologia do ^ etc? acredito que seja algo sobre erro acumulado ou algo assim, nao?
esse tipo de informação é extremamente crucial para mim no relatorio, para ir entendendo as demonstrações com as coisas
"frescas" pois acabamos de ler, entende?

RESPOSTA — a mesma reta com três roupas:

    linreg.py         y = a·X + b          a = inclinação,  b = intercepto
    aqui              ŷ = β₀ + β₁·x        β₁ = inclinação, β₀ = intercepto
    folha do prof.    φ(x) = β₁·x + β₂     β₁ = inclinação, β₂ = intercepto

  O chapéu (^) NÃO é erro acumulado. Ele separa duas coisas:
    β₁   (sem chapéu) = a inclinação "verdadeira" do processo que gera os
                        dados — ninguém conhece, é o que queremos descobrir.
    β̂₁  (com chapéu) = a ESTIMATIVA dela, calculada a partir desta amostra.
    ŷ    = o valor que o MODELO prevê;  y = o valor que foi OBSERVADO.
  Outra amostra de 10.000 dias daria um β̂₁ um pouco diferente; o β₁ não muda.

  Onde entra o erro acumulado: E(β₀,β₁) = Σ(yᵢ − β₀ − β₁xᵢ)² é a FUNÇÃO que
  se minimiza (a "bacia" do linreg.py, um paraboloide sobre o plano β₀×β₁).
  β̂₀ e β̂₁ são as coordenadas do FUNDO da bacia. Ou seja: o chapéu marca o
  resultado da minimização, e o erro acumulado é o que foi minimizado.

Minimizando o erro acumulado E(β₀,β₁) = Σ(yᵢ − β₀ − β₁xᵢ)² , as derivadas
parciais igualadas a zero dão as EQUAÇÕES NORMAIS, cuja solução é:

        Sxy                          n·Σxy − Σx·Σy
  β₁ = -----      (equivalente a    ---------------- )
        Sxx                          n·Σx² − (Σx)²

  β₀ = ȳ − β₁·x̄

onde, com x̄ e ȳ sendo as médias:

  Sxx = Σ(xᵢ − x̄)²            "variância não normalizada de x"
  Sxy = Σ(xᵢ − x̄)(yᵢ − ȳ)     "covariância não normalizada"
tipo, isso de variancia eu lembro que é aquela medida entre media-x x media+x algo assim, nao?
e covariancia? e como ler melhor essa relação?

RESPOSTA:
  VARIÂNCIA é a distância ao quadrado de cada ponto até a média, em média:
      Var(x) = Σ(xᵢ − x̄)² / n        →   Sxx = n · Var(x)  ("não normalizada")
  O "média−σ até média+σ" que você lembra é a FAIXA do desvio padrão
  (σ = √Var): numa distribuição normal, ~68% dos pontos caem ali. É uma
  consequência da variância, não a definição dela.

  COVARIÂNCIA pergunta se x e y se afastam da média JUNTOS:
      Sxy = Σ(xᵢ − x̄)(yᵢ − ȳ)
  Cada termo é um produto de dois desvios. Ponto com x acima da média E y
  acima → (+)(+) = +. Os dois abaixo → (−)(−) = +. Um acima e outro abaixo
  → negativo. Somando tudo: Sxy > 0 quando "x maior costuma vir com y maior"
  (o disco: dia maior, uso maior), Sxy < 0 quando é o contrário, ≈ 0 quando
  não há relação linear.

  Lendo a fórmula do β̂₁ = Sxy / Sxx:
      "quanto y anda junto com x"  ÷  "quanto x varia sozinho"
  = quanto y muda, em média, por unidade de x. Exatamente o que uma
  inclinação é — aqui, GB por dia.

Duas consequências que viram teste mais abaixo:

  (I)  β₀ = ȳ − β₁x̄  implica  β₀ + β₁x̄ = ȳ
       -> a reta passa OBRIGATORIAMENTE pelo centro de massa (x̄, ȳ). Sempre.
       tem como ver isso? nao sei se consegui visualizar bem o que significam as variaveis e a reta no centro de massa

       RESPOSTA: sim — figuras/02_reta_centro_massa.png, gerada no fim deste
       arquivo. O centro de massa é o ponto (x̄, ȳ): o "dia médio" (5000,5) e a
       "ocupação média" (2370,8 GB). Desenhe as duas linhas tracejadas x = x̄
       e y = ȳ: a reta ajustada passa exatamente no cruzamento delas. Intuição:
       Σeᵢ = 0 diz que os resíduos acima e abaixo da reta se cancelam — a reta
       fica "equilibrada" no meio da nuvem, como uma régua apoiada no ponto de
       equilíbrio. Qualquer reta que não passasse por ali teria mais pontos de
       um lado do que do outro, e Σe ≠ 0.

  (II) As equações normais são, literalmente,  Σeᵢ = 0  e  Σxᵢeᵢ = 0,
       com eᵢ = yᵢ − ŷᵢ. Não é propriedade do dataset: é o que "derivada igual
       a zero" significa. Isso volta na Etapa 3 e é o que faz o R² existir.

===============================================================================
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# sklearn é só a REFERÊNCIA da verificação V5. Import protegido: nesta máquina
# o Controle Inteligente de Aplicativos do Windows bloqueia a DLL do sklearn;
# no Colab (ou com o bloqueio desligado) a V5 roda normalmente.
try:
    from sklearn.linear_model import LinearRegression
except ImportError:
    LinearRegression = None

# --- dados (encanamento pronto) ----------------------------------------------
AQUI = Path(__file__).parent
FIGURAS = AQUI / "figuras"
FIGURAS.mkdir(exist_ok=True)
df = pd.read_csv(AQUI / "monitoramento_disco_10k_v2.csv")

x = df["dia"].values.astype(float)
y = df["uso_disco_gb"].values


# =============================================================================
# FERRAMENTAS DISPONÍVEIS (vocabulário, não receita)
# =============================================================================
#   np.mean(v)          média dos elementos
#   np.sum(v)           soma dos elementos
#   np.dot(u, v)        produto escalar: Σ uᵢ·vᵢ
#   len(v)              quantidade de elementos
#
#   Arrays NumPy operam ELEMENTO A ELEMENTO, sem laço:
#       v - 3           subtrai 3 de cada elemento
#       u * v           multiplica posição a posição
#       v ** 2          eleva cada elemento ao quadrado
#
#   Você não precisa de nenhum `for` neste arquivo.
# =============================================================================


def calcular_sxx(x):
    """Soma dos desvios quadráticos de x em relação à sua média.

    Sxx = Σ (xᵢ − x̄)²

    Parâmetros
    ----------
    x : np.ndarray  — valores da variável independente

    Retorna
    -------
    float — um número só (não um array)
    """
    # Tentativa original:  np.dot(np.ndarray(x), np.mean(np.ndarray(x)))**2
    # Dois erros: (1) np.ndarray é a CLASSE e espera um formato (shape), não
    # dados — e x já é array, não precisa converter; (2) o quadrado estava
    # FORA da soma, (Σ…)², e a fórmula pede Σ(…)². A intuição do np.dot estava
    # certa: faltava o array de DESVIOS.
    desvios = x - np.mean(x)
    return np.dot(desvios, desvios)          # = Σ (xᵢ − x̄)²


def calcular_sxy(x, y):
    """Soma dos produtos dos desvios de x e y em relação às suas médias.

    Sxy = Σ (xᵢ − x̄)(yᵢ − ȳ)

    Parâmetros
    ----------
    x, y : np.ndarray — mesmo comprimento

    Retorna
    -------
    float
    """
    # Tentativa original montava TUPLAS (x, x̄) em vez de subtrair x − x̄.
    # A estrutura certa é a mesma do Sxx, com dois arrays de desvios diferentes.
    return np.dot(x - np.mean(x), y - np.mean(y))   # = Σ (xᵢ − x̄)(yᵢ − ȳ)


def ajustar(x, y):
    """Ajusta a reta de mínimos quadrados.

    Deve usar calcular_sxx e calcular_sxy — não reimplemente os somatórios.

        β₁ = Sxy / Sxx
        β₀ = ȳ − β₁·x̄

    Retorna
    -------
    (beta0, beta1) : tuple[float, float]   — NESTA ordem (intercepto primeiro)
    """
    b1 = calcular_sxy(x, y) / calcular_sxx(x)
    # essa aqui eu esqueci b0 =
    # → β₀ = ȳ − β₁·x̄ : sai do teorema do centro de massa (a reta passa por (x̄, ȳ)).
    b0 = np.mean(y) - b1 * np.mean(x)
    return b0, b1


def prever(x, beta0, beta1):
    """Aplica a reta ajustada.

    ŷᵢ = β₀ + β₁·xᵢ

    Retorna
    -------
    np.ndarray — mesmo comprimento de x
    """
    return beta0 + beta1 * x


def estimar_beta1_por_blocos(x, y, tamanho=500):
    """Inclinação grosseira por uma reta de DOIS pontos.

    Ideia: comparar o "nível médio" do início da série com o do fim.

        ponto A = (média de x nos primeiros `tamanho`,  média de y neles)
        ponto B = (média de x nos últimos  `tamanho`,   média de y neles)
        inclinação = (y_B − y_A) / (x_B − x_A)

    Não é mínimos quadrados — é um sanity check de ORDEM DE GRANDEZA.
    (Dica de fatiamento: v[:k] pega os k primeiros, v[-k:] pega os k últimos.)

    Retorna
    -------
    float
    """
    x_a, y_a = np.mean(x[:tamanho]), np.mean(y[:tamanho])
    x_b, y_b = np.mean(x[-tamanho:]), np.mean(y[-tamanho:])
    return (y_b - y_a) / (x_b - x_a)


# =============================================================================
# CAMINHO 2 — a forma matricial da folha do professor
# =============================================================================
# A folha resolve o MESMO problema escrevendo as n equações  β₁xᵢ + β₂ = yᵢ
# como um sistema  C·β = y :
#
#        ⎡ x₁  1 ⎤            ⎡ y₁ ⎤
#    C = ⎢ x₂  1 ⎥   β = ⎡β₁⎤  y = ⎢ y₂ ⎥        (n equações, 2 incógnitas:
#        ⎢ ⋮   ⋮ ⎥       ⎣β₂⎦      ⎢ ⋮  ⎥         sem solução exata)
#        ⎣ xₙ  1 ⎦                 ⎣ yₙ ⎦
#
# Multiplicando os dois lados por Cᵀ:   CᵀC·β = Cᵀy   →   A·β = b
#
#    A = CᵀC = ⎡ Σx²  Σx ⎤        b = Cᵀy = ⎡ Σxy ⎤
#              ⎣ Σx    n ⎦                  ⎣ Σy  ⎦
#
# A·β = b são LITERALMENTE as equações normais da derivação do linreg.py
# (∂E/∂β₁ = 0 e ∂E/∂β₂ = 0). Mesma matemática, outra escrita — por isso o
# resultado tem que ser idêntico ao do Caminho 1 (verificação V7).
#
# O que a forma matricial ganha: com mais variáveis de entrada, basta pôr mais
# colunas em C. As fórmulas Sxy/Sxx do Caminho 1 só existem para UMA variável.
#
# Atenção à ordem: a folha usa β = [β₁, β₂] = [inclinação, intercepto], ao
# contrário do (β₀, β₁) deste arquivo. A função devolve NA ORDEM DESTE ARQUIVO.

def ajustar_matricial(x, y):
    """Mesmo ajuste, pelo método da folha. Retorna (beta0, beta1)."""
    C = np.column_stack([x, np.ones(len(x))])
    A = C.T @ C
    b = C.T @ y
    beta1, beta2 = np.linalg.solve(A, b)        # ordem da folha: [inclinação, intercepto]
    return beta2, beta1                          # ordem deste arquivo: (β₀, β₁)


# =============================================================================
# VERIFICAÇÃO — roda sozinha. Nenhuma checagem contém a resposta numérica.
# =============================================================================

def verificar():
    n = len(x)
    passou, total = 0, 8

    def checa(rotulo, condicao, detalhe=""):
        nonlocal passou
        if condicao:
            passou += 1
            print(f"  [OK]    {rotulo}")
        else:
            print(f"  [FALHA] {rotulo}  {detalhe}")

    print("=" * 70)

    # --- V1: Sxx contra a FORMA FECHADA para x = 1..n -------------------------
    # Como x é a sequência 1..n, sabemos Sxx sem olhar os dados:
    #   Sxx = n · Var_pop(1..n) = n(n² − 1)/12
    # (é o mesmo (n²−1)/12 do Checkpoint 1 do 01_eda.py, multiplicado por n)
    try:
        sxx = calcular_sxx(x)
        esperado = n * (n**2 - 1) / 12
        checa("V1  Sxx bate com a forma fechada n(n²−1)/12",
              np.isclose(sxx, esperado, rtol=1e-9),
              f"seu={sxx:.4f} fórmula={esperado:.4f}")
    except NotImplementedError as e:
        checa("V1  Sxx bate com a forma fechada n(n²−1)/12", False, f"({e} não implementada)")

    # --- V2: Sxy por dois caminhos algebricamente equivalentes ----------------
    # Expandindo Σ(xᵢ−x̄)(yᵢ−ȳ) chega-se a Σxᵢyᵢ − n·x̄·ȳ.
    # Se sua implementação bate com a forma expandida, a álgebra está certa —
    # e isso não revela QUANTO dá.
    try:
        sxy = calcular_sxy(x, y)
        forma_expandida = np.dot(x, y) - n * np.mean(x) * np.mean(y)
        checa("V2  Sxy bate com a forma expandida Σxy − n·x̄·ȳ",
              np.isclose(sxy, forma_expandida, rtol=1e-9),
              f"seu={sxy:.4f} expandida={forma_expandida:.4f}")
    except NotImplementedError as e:
        checa("V2  Sxy bate com a forma expandida Σxy − n·x̄·ȳ", False, f"({e} não implementada)")

    # --- V3: o teorema do centro de massa ------------------------------------
    # β₀ + β₁·x̄ = ȳ, sempre. Teste INDEPENDENTE de qualquer biblioteca.
    try:
        b0, b1 = ajustar(x, y)
        checa("V3  a reta passa pelo centro de massa (β₀ + β₁·x̄ = ȳ)",
              np.isclose(b0 + b1 * np.mean(x), np.mean(y), rtol=1e-9))
    except NotImplementedError as e:
        checa("V3  a reta passa pelo centro de massa (β₀ + β₁·x̄ = ȳ)", False,
              f"({e} não implementada)")

    # --- V4: as equações normais (Σe = 0 e Σxe = 0) ---------------------------
    # Não é coincidência do dataset: é a DEFINIÇÃO de "derivada igual a zero".
    # Se falhar aqui mas V3 passar, o erro está em `prever`.
    try:
        b0, b1 = ajustar(x, y)
        e = y - prever(x, b0, b1)
        escala = np.abs(y).mean() * len(y)
        checa("V4  equações normais: Σeᵢ ≈ 0  e  Σxᵢeᵢ ≈ 0",
              abs(np.sum(e)) / escala < 1e-10 and abs(np.dot(x, e)) / (escala * np.abs(x).mean()) < 1e-10,
              f"Σe={np.sum(e):.3e}  Σxe={np.dot(x, e):.3e}")
    except NotImplementedError as e:
        checa("V4  equações normais: Σeᵢ ≈ 0  e  Σxᵢeᵢ ≈ 0", False, f"({e} não implementada)")

    # --- V5: concordância com a implementação de referência -------------------
    # A sklearn resolve o mesmo sistema por outro caminho numérico.
    if LinearRegression is None:
        total -= 1
        print("  [PULADA] V5  sklearn indisponível nesta máquina (bloqueio do Windows)")
    else:
        b0, b1 = ajustar(x, y)
        ref = LinearRegression().fit(x.reshape(-1, 1), y)
        checa("V5  coincide com sklearn.LinearRegression",
              np.isclose(b0, ref.intercept_) and np.isclose(b1, ref.coef_[0]),
              f"seu=({b0:.6f}, {b1:.6f}) sklearn=({ref.intercept_:.6f}, {ref.coef_[0]:.6f})")

    # --- V6: ordem de grandeza contra a reta de dois pontos -------------------
    # Tolerância folgada de propósito: é sanity check, não precisão.
    try:
        _, b1 = ajustar(x, y)
        grosseiro = estimar_beta1_por_blocos(x, y)
        razao = b1 / grosseiro
        checa("V6  β₁ na mesma ordem de grandeza da reta de dois pontos",
              0.5 < razao < 2.0, f"razão={razao:.4f} (esperado ≈ 1)")
    except NotImplementedError as e:
        checa("V6  β₁ na mesma ordem de grandeza da reta de dois pontos", False,
              f"({e} não implementada)")

    # --- V7: forma matricial (folha) × fórmulas Sxy/Sxx -----------------------
    # Dois caminhos algebricamente idênticos: têm que concordar até o arredondamento.
    b0, b1 = ajustar(x, y)
    m0, m1 = ajustar_matricial(x, y)
    checa("V7  forma matricial (CᵀCβ = Cᵀy) == fórmulas Sxy/Sxx",
          np.isclose(b0, m0, rtol=1e-9) and np.isclose(b1, m1, rtol=1e-9),
          f"fórmulas=({b0:.8f}, {b1:.10f}) matricial=({m0:.8f}, {m1:.10f})")

    # --- V8: o mesmo código reproduz a página 3 da folha ----------------------
    # Os 4 pontos do exemplo de aula; a folha chega a φ(x) = 1,97188755·x + 1,807228916.
    x4 = np.array([1.2, 2.3, 3.5, 4.7])
    y4 = np.array([4.0, 6.8, 8.3, 11.2])
    p0, p1 = ajustar_matricial(x4, y4)
    checa("V8  4 pontos da folha → β₁ = 1,97188755 e β₂ = 1,807228916",
          np.isclose(p1, 1.97188755, atol=1e-8) and np.isclose(p0, 1.807228916, atol=1e-8),
          f"β₁={p1:.9f} β₂={p0:.9f}")

    print("=" * 70)
    print(f"  {passou}/{total} verificações OK")
    print("=" * 70)
    return passou == total


if __name__ == "__main__":
    tudo_ok = verificar()

    if tudo_ok:
        b0, b1 = ajustar(x, y)
        print(f"\nEquação ajustada:  ŷ = {b0:.4f} + {b1:.6f}·x\n")

        # =====================================================================
        # INTERPRETAÇÃO (item 2.3 do enunciado) — sem código, só raciocínio
        # =====================================================================
        # TODO(I1): β₁ tem unidade. Qual? Converta para uma unidade que um
        #   gestor de TI entenda (GB/mês, GB/ano) e escreva a frase que iria
        #   no relatório — do tipo "o servidor consome ___ por mês".
        #
        #   # >>> RESPOSTA: β₁ está em GB/dia (y em GB dividido por x em dias).
        #   #     0,4486 GB/dia ≈ 13,5 GB/mês ≈ 164 GB/ano.
        #   #     Frase: "o servidor consome em média 13,5 GB por mês, ou
        #   #     cerca de 164 GB por ano".
        print(f"I1  β₁ = {b1:.6f} GB/dia ≈ {b1 * 30:.2f} GB/mês ≈ {b1 * 365:.1f} GB/ano")
        #
        # TODO(I2): β₀ é a ocupação prevista no DIA 0, que não existe no
        #   dataset (a série começa no dia 1). Duas leituras possíveis:
        #     (a) "é o quanto o disco já tinha ocupado antes do monitoramento"
        #     (b) "é só onde a reta cruza o eixo, sem significado físico"
        #   Qual você defende, e por quê? A resposta depende de o dia 0 estar
        #   PERTO ou LONGE do intervalo observado — argumente a partir disso.
        #
        #   # >>> RESPOSTA: (a), com ressalva. O dia 0 está a UM dia do início
        #   #     dos dados — extrapolação mínima, então β₀ ≈ 127,65 GB é uma
        #   #     leitura razoável de "ocupação de base quando o monitoramento
        #   #     ligou" (sistema operacional, aplicações instaladas). Seria (b)
        #   #     se o dia 0 estivesse longe da faixa observada (ex.: x = ano
        #   #     2024, onde "ano 0" não tem sentido físico). Ressalva: o piso
        #   #     artificial do início puxa β₀ para cima (ver I4).
        print(f"I2  β₀ = {b0:.2f} GB (ocupação prevista no dia 0)")
        #
        # TODO(I3): compare β₀ + β₁ (previsão para o dia 1) com y[0] (o valor
        #   observado no dia 1). Eles batem? DEVERIAM bater? O que a diferença
        #   entre os dois representa?
        #
        #   # >>> RESPOSTA: não batem (128,10 previsto × 233,93 observado) e
        #   #     NÃO deveriam bater. A reta é a ocupação MÉDIA esperada para o
        #   #     dia 1; o valor observado é a média + o ruído daquele dia. A
        #   #     diferença, +105,8 GB, é o RESÍDUO e₁ — o mesmo ruído diário de
        #   #     ±~228 GB que a Etapa 3 vai medir. Um dia isolado bater com a
        #   #     reta seria coincidência.
        prev_d1 = prever(x[0], b0, b1)
        print(f"I3  dia 1: previsto {prev_d1:.2f} GB × observado {y[0]:.2f} GB "
              f"→ resíduo e₁ = {y[0] - prev_d1:+.2f} GB")
        #
        # TODO(I4): lembre do PISO que você achou na Etapa 1 (101 registros
        #   travados em 10 GB, dias 14 a 1102). Eles estão todos no INÍCIO da
        #   série — justamente onde o intercepto é determinado. Em que direção
        #   isso empurra β₀: para cima ou para baixo? Pense no que o corte faz
        #   com os valores que "queriam" ser menores.
        #   Depois teste: reajuste usando só os dias > 1102 e compare.
        #
        #   # >>> RESPOSTA: para CIMA. Os dias que "queriam" ficar abaixo de
        #   #     10 GB foram levantados até 10 GB — o corte só sobe valores,
        #   #     nunca desce. Pontos artificialmente altos no começo da série
        #   #     levantam a ponta esquerda da reta, ou seja, o intercepto.
        #   #     Teste: sem os dias ≤ 1102, β₀ cai de 127,65 para 121,25 GB
        #   #     (−6,4 GB) e β₁ muda só +0,21%. Conclusão: o efeito existe, na
        #   #     direção prevista, mas é pequeno — o modelo completo fica, com a
        #   #     censura declarada como ressalva.
        sem_censura = x > 1102
        s0, s1 = ajustar(x[sem_censura], y[sem_censura])
        print(f"I4  sem os dias ≤ 1102: β₀ = {s0:.2f} GB ({s0 - b0:+.2f}),  "
              f"β₁ = {s1:.6f} ({100 * (s1 - b1) / b1:+.2f}%)")

        # --- A forma matricial da folha, lado a lado --------------------------
        m0, m1 = ajustar_matricial(x, y)
        print(f"\nFórmulas Sxy/Sxx : ŷ = {b0:.8f} + {b1:.10f}·x")
        print(f"Forma matricial  : ŷ = {m0:.8f} + {m1:.10f}·x")
        n = len(x)
        C = np.column_stack([x, np.ones(n)])
        print(f"cond(CᵀC) = {np.linalg.cond(C.T @ C):.3g}  "
              "(com os 4 pontos da folha: ≈ 72)")
        # Por que olhar o número de condição: com x indo até 10.000, Σx² ≈ 3,3·10¹¹
        # convive com n = 10⁴ dentro da mesma matriz A. Em precisão dupla o
        # resultado ainda sai certo (V7 passou), mas é por isso que bibliotecas
        # como np.linalg.lstsq resolvem C·β ≈ y direto, sem montar CᵀC.

        # --- Figura: a reta passa pelo centro de massa (sua pergunta acima) ----
        x_bar, y_bar = np.mean(x), np.mean(y)
        amostra = np.random.default_rng(42).choice(n, size=1000, replace=False)
        fig, ax = plt.subplots(figsize=(9, 5.5))
        ax.scatter(x[amostra], y[amostra], s=10, alpha=0.5, color="gray",
                   label="amostra de 1.000 dias")
        ax.plot(x, prever(x, b0, b1), color="tab:red", linewidth=2,
                label=f"ŷ = {b0:.2f} + {b1:.4f}·x")
        ax.axvline(x_bar, color="tab:blue", linestyle="--", linewidth=1, label=f"x̄ = {x_bar:.1f}")
        ax.axhline(y_bar, color="tab:green", linestyle="--", linewidth=1, label=f"ȳ = {y_bar:.1f} GB")
        ax.scatter(x_bar, y_bar, marker="X", s=180, color="black", zorder=4,
                   label="centro de massa (x̄, ȳ)")
        ax.set_title("A reta de mínimos quadrados passa pelo centro de massa")
        ax.set_xlabel("dia")
        ax.set_ylabel("uso_disco_gb (GB)")
        ax.legend(loc="upper left")
        ax.grid(alpha=0.3)
        fig.tight_layout()
        fig.savefig(FIGURAS / "02_reta_centro_massa.png", dpi=150)
        plt.show()


# =============================================================================
# DICAS — leia só depois de travar de verdade. Conceito, não código.
# =============================================================================
#
# calcular_sxx:
#   `x - np.mean(x)` já devolve um ARRAY com todos os desvios de uma vez.
#   Você só precisa elevar ao quadrado e somar. Sem laço.
#
# calcular_sxy:
#   Mesma ideia, com dois arrays de desvios multiplicados posição a posição.
#   (`np.dot` faz "multiplica e soma" num passo só, se preferir.)
#
# ajustar:
#   São duas linhas de conta mais o `return`. A ordem importa: β₁ primeiro,
#   porque β₀ depende dele.
#   Para devolver dois valores: `return primeiro, segundo`.
#
# prever:
#   Aritmética de array: `beta1 * x` já multiplica cada elemento.
#
# estimar_beta1_por_blocos:
#   Quatro médias (x e y, no início e no fim), depois uma divisão.
#   Fatiar: `x[:tamanho]` e `x[-tamanho:]`.
#
# Erro comum: esquecer o `return` e a função devolver None silenciosamente —
# o sintoma é `TypeError: cannot unpack non-sequence NoneType`.
