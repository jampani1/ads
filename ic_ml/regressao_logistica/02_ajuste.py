"""
02_ajuste.py — Item 5: ajustar a regressão logística
Atividade de IC: Classificação de entregas por Regressão Logística.

===============================================================================
MATEMÁTICA DA ETAPA — do log da chance à máxima verossimilhança
===============================================================================

1) O MODELO. Precisamos de algo que vá de −∞ a +∞ para poder igualar a uma reta.

    p                ∈ (0, 1)      probabilidade
    p / (1 − p)      ∈ (0, ∞)      chance (odds): p = 0,8 é chance de 4 para 1
    ln(p / (1 − p))  ∈ (−∞, ∞)     log da chance (logit)

  Igualando o logit à reta do enunciado:

    ln(p / (1 − p)) = Z(x) = β₀ + β₁x

  e isolando p:

    p/(1−p) = e^Z  →  p = e^Z − p·e^Z  →  p(1 + e^Z) = e^Z
    p = e^Z / (1 + e^Z) = 1 / (1 + e^(−Z))         ← a sigmoide do enunciado

  A reta continua lá dentro: ela é o Z. A sigmoide só a "dobra" para caber em (0, 1).

2) O CRITÉRIO. Por que não mínimos quadrados? Porque aqui o critério natural vem da
  distribuição de y. Cada pedido é uma Bernoulli, com probabilidade do que aconteceu:

    P(yᵢ | xᵢ) = pᵢ^yᵢ · (1 − pᵢ)^(1 − yᵢ)

  (se yᵢ = 1 sobra pᵢ; se yᵢ = 0 sobra 1 − pᵢ). Com pedidos independentes, a
  probabilidade da amostra inteira é o produto: a VEROSSIMILHANÇA L(β). O logaritmo
  troca produto por soma sem mudar onde está o máximo:

    ℓ(β) = Σ [ yᵢ·ln(pᵢ) + (1 − yᵢ)·ln(1 − pᵢ) ]

  "Otimizar" (item 5a) é achar o β que torna o que foi observado o mais provável.
  −ℓ é a entropia cruzada, a mesma função de perda das redes neurais.

3) O GRADIENTE. A sigmoide tem uma derivada particular: dp/dZ = p(1 − p). Com ela e a
  regra da cadeia, os termos se cancelam e sobra:

    ∂ℓ/∂β₀ = Σ (yᵢ − pᵢ)
    ∂ℓ/∂β₁ = Σ (yᵢ − pᵢ)·xᵢ          na forma matricial:  ∇ℓ = Cᵀ(y − p)

  com C = [1 x]. Compare com a regressão linear, em que ∇ = 2Cᵀ(y − Cβ): é a MESMA
  estrutura, "resíduo vezes entrada". A diferença é que aqui p = σ(Cβ) não é linear
  em β, então ∇ℓ = 0 não dá um sistema linear. NÃO EXISTE FÓRMULA FECHADA.

4) A SOLUÇÃO. Derivando de novo, a matriz hessiana:

    H = −Cᵀ W C        W = diag(pᵢ(1 − pᵢ))

  H é negativa definida (se C tem posto cheio e nenhum pᵢ é 0 ou 1): ℓ é CÔNCAVA.
  Só existe um topo, nenhum máximo local para atrapalhar. Dois jeitos de subir:

  Subida de gradiente:   β ← β + α·∇ℓ
      anda na direção de maior subida, com passo fixo α. Só usa a inclinação.

  Newton-Raphson:        β ← β + (CᵀWC)⁻¹ Cᵀ(y − p)
      aproxima ℓ por uma parábola e pula para o topo dela. Usa também a curvatura.

  Cada passo de Newton resolve  (CᵀWC)·Δ = Cᵀ(y − p), que é o sistema da folha do
  orientador, CᵀC·β = Cᵀy, com pesos. Por isso o método também se chama IRLS
  (mínimos quadrados reponderados iterativamente).

  Saindo de β = 0, todo pᵢ = 1/2 e todo peso é 1/4. O primeiro passo vira então

      β⁽¹⁾ = 4·(CᵀC)⁻¹Cᵀ(y − 1/2)

  ou seja, QUATRO VEZES A RETA DE MÍNIMOS QUADRADOS ajustada em y − 1/2. A regressão
  logística começa, literalmente, na regressão linear. A verificação V8 confere isso.

5) INCERTEZA. Perto do ótimo, Var(β̂) ≈ (CᵀWC)⁻¹ (inversa da curvatura: topo pontudo
  significa estimativa precisa). Daí vêm o erro padrão e o intervalo de Wald. O teste
  de razão de verossimilhança compara ℓ do modelo com ℓ do modelo sem x:

      D = 2·(ℓ_modelo − ℓ_nulo)  ~  χ² com 1 grau de liberdade

===============================================================================
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

import comum
from comum import COR_APOIO, COR_ATRASO, COR_CORRETA, COR_GRADE, COR_MODELO, FIGURAS, br

df = comum.carregar_dados()
x = df["x"].values
y = df["y"].values
n = len(y)


# ==============================================================================
# Funções do modelo
# ==============================================================================
def sigmoide(z):
    """σ(z) = 1 / (1 + e^(−z))."""
    return 1.0 / (1.0 + np.exp(-z))


def matriz_c(x):
    """C = [1 x]. A coluna de 1 é a que multiplica β₀ (ordem do enunciado: β₀, β₁)."""
    return np.column_stack([np.ones(len(x)), x])


def log_verossimilhanca(beta, C, y):
    """
    ℓ(β) = Σ [y·ln(p) + (1−y)·ln(1−p)], escrita como Σ [y·Z − ln(1 + e^Z)].

    As duas formas são iguais; a segunda não calcula ln(0) quando p encosta em 0 ou 1.
    `np.logaddexp(0, Z)` é ln(1 + e^Z) sem estourar para Z grande.
    """
    Z = C @ beta
    return float(np.sum(y * Z - np.logaddexp(0, Z)))


def gradiente(beta, C, y):
    """∇ℓ = Cᵀ(y − p)."""
    return C.T @ (y - sigmoide(C @ beta))


def hessiana(beta, C):
    """H = −CᵀWC, com W = diag(p(1 − p))."""
    p = sigmoide(C @ beta)
    pesos = p * (1 - p)
    return -(C.T * pesos) @ C              # (C.T * pesos) multiplica cada coluna de Cᵀ pelo peso


def ajustar_newton(x, y, tol=1e-10, max_iter=100):
    """Newton-Raphson a partir de β = 0. Devolve (β, trajetória)."""
    C = matriz_c(x)
    beta = np.zeros(2)
    trajetoria = [beta.copy()]
    for _ in range(max_iter):
        passo = np.linalg.solve(-hessiana(beta, C), gradiente(beta, C, y))
        beta = beta + passo
        trajetoria.append(beta.copy())
        if np.max(np.abs(passo)) < tol:
            break
    return beta, np.array(trajetoria)


def ajustar_gradiente(x, y, alfa=0.0008, tol=1e-6, max_iter=2_000_000):
    """
    Subida de gradiente a partir de β = 0. Devolve (β, trajetória, iterações).

    α precisa ficar abaixo de 2/λ_max, com λ_max o maior autovalor de CᵀWC: em β = 0
    ele vale cerca de 2.000, o que limita α a ~0,001. É a escala de x² dentro de CᵀC.
    """
    C = matriz_c(x)
    beta = np.zeros(2)
    trajetoria = [beta.copy()]
    for i in range(1, max_iter + 1):
        g = gradiente(beta, C, y)
        beta = beta + alfa * g
        if i <= 200 or i % 200 == 0:       # guarda só o suficiente para desenhar
            trajetoria.append(beta.copy())
        if np.max(np.abs(g)) < tol:
            break
    return beta, np.array(trajetoria), i


def prever_p(valores_x, beta):
    """p(x) para um escalar ou array de antecedências."""
    return sigmoide(beta[0] + beta[1] * np.asarray(valores_x, dtype=float))


# ==============================================================================
# Execução
# ==============================================================================
if __name__ == "__main__":
    C = matriz_c(x)

    # --- item 5a: otimização -----------------------------------------------------
    beta, traj_newton = ajustar_newton(x, y)
    beta_gd, traj_gd, iter_gd = ajustar_gradiente(x, y)
    b0, b1 = beta
    iter_newton = len(traj_newton) - 1
    p = sigmoide(C @ beta)

    print("=== Item 5a — otimização ===")
    print(f"{'iter':>4} {'β₀':>12} {'β₁':>12} {'ℓ(β)':>12}")
    for i, b in enumerate(traj_newton):
        print(f"{i:>4} {b[0]:>12.8f} {b[1]:>12.8f} {log_verossimilhanca(b, C, y):>12.6f}")
    print(f"\nNewton            : {iter_newton} iterações")
    print(f"Subida de gradiente: {iter_gd:,} iterações, β = ({beta_gd[0]:.6f}, {beta_gd[1]:.6f})")

    # --- verificações ------------------------------------------------------------
    # Nenhuma compara com valor esperado: cada uma confere uma identidade matemática.
    def derivada_numerica(f, b, h=1e-6):
        return np.array([(f(b + h * e) - f(b - h * e)) / (2 * h) for e in np.eye(2)])

    print("\n=== Verificações ===")
    checagens = []

    def checar(nome, condicao):
        checagens.append(bool(condicao))
        print(f"  [{'OK' if condicao else 'FALHA'}]{'  ' if condicao else ' '}  {nome}")

    z = np.linspace(-6, 6, 25)
    checar("V1  σ(0) = 1/2  e  σ(−z) = 1 − σ(z)",
           sigmoide(0.0) == 0.5 and np.allclose(sigmoide(-z), 1 - sigmoide(z)))

    teste = np.array([-1.0, 0.1])
    g_num = derivada_numerica(lambda b: log_verossimilhanca(b, C, y), teste)
    checar("V2  gradiente analítico = derivada numérica de ℓ",
           np.allclose(gradiente(teste, C, y), g_num, atol=1e-5))

    h_num = np.column_stack([derivada_numerica(lambda b, k=k: gradiente(b, C, y)[k], teste)
                             for k in range(2)])
    checar("V3  hessiana analítica = derivada numérica do gradiente",
           np.allclose(hessiana(teste, C), h_num, atol=1e-4))

    checar("V4  equações de escore no ótimo: Σ(y − p) ≈ 0  e  Σx(y − p) ≈ 0",
           np.allclose(gradiente(beta, C, y), 0, atol=1e-9))

    autovalores = np.linalg.eigvalsh(hessiana(beta, C))
    checar("V5  hessiana negativa definida (ℓ é côncava: o topo é único)",
           np.all(autovalores < 0))

    checar("V6  subida de gradiente chega ao mesmo β de Newton",
           np.allclose(beta, beta_gd, atol=1e-5))

    beta_sklearn = None
    try:
        from sklearn.linear_model import LogisticRegression
        X2 = x.reshape(-1, 1)
        # C é o INVERSO da força da penalidade: C = ∞ desliga a regularização.
        m = LogisticRegression(C=np.inf, tol=1e-10, max_iter=10_000).fit(X2, y)
        beta_sklearn = np.array([m.intercept_[0], m.coef_[0, 0]])
        padrao = LogisticRegression().fit(X2, y)
        beta_padrao = np.array([padrao.intercept_[0], padrao.coef_[0, 0]])
        checar("V7  coincide com sklearn LogisticRegression(C=np.inf)",
               np.allclose(beta, beta_sklearn, atol=1e-5))
    except ImportError:
        print("  [PULADA] V7  scikit-learn indisponível")

    primeiro_passo = traj_newton[1]
    reta = np.linalg.solve(C.T @ C, C.T @ (y - 0.5))
    checar("V8  1º passo de Newton = 4 × reta de mínimos quadrados em y − 1/2",
           np.allclose(primeiro_passo, 4 * reta))

    print(f"\n{sum(checagens)}/{len(checagens)} verificações")
    assert all(checagens)

    print("\nConsequência da V4 (a primeira equação de escore):")
    print(f"Σp = {p.sum():.6f}   Σy = {y.sum()}  → o modelo prevê exatamente o nº de entregas corretas")

    if beta_sklearn is not None:
        print("\n=== sklearn: padrão × sem penalidade ===")
        print(f"mão (máxima verossimilhança): β₀ = {b0:.6f}   β₁ = {b1:.6f}")
        print(f"sklearn C=np.inf             : β₀ = {beta_sklearn[0]:.6f}   β₁ = {beta_sklearn[1]:.6f}")
        print(f"sklearn padrão (C=1, L2)     : β₀ = {beta_padrao[0]:.6f}   β₁ = {beta_padrao[1]:.6f}")
        print(f"diferença do padrão em β₁    : {(beta_padrao[1] / b1 - 1):+.2%}")

    # --- item 5b: coeficientes e funções -----------------------------------------
    print("\n=== Item 5b — funções ajustadas ===")
    print(f"Z(x) = {b0:.4f} + {b1:.4f}·x")
    print(f"p(x) = 1 / (1 + e^(−({b0:.4f} + {b1:.4f}·x)))")

    # --- item 5c: sinal de β₁ ----------------------------------------------------
    variancia = np.linalg.inv(-hessiana(beta, C))
    ep = np.sqrt(np.diag(variancia))
    z_wald = beta / ep
    z_crit = stats.norm.ppf(0.975)
    ic_b1 = (b1 - z_crit * ep[1], b1 + z_crit * ep[1])
    razao_chance = np.exp(b1)
    ic_rc = np.exp(ic_b1)

    p_nulo = y.mean()
    ell = log_verossimilhanca(beta, C, y)
    ell_nulo = float(np.sum(y * np.log(p_nulo) + (1 - y) * np.log(1 - p_nulo)))
    D = 2 * (ell - ell_nulo)
    valor_p = stats.chi2.sf(D, df=1)
    r2_mcfadden = 1 - ell / ell_nulo
    x_meio = -b0 / b1

    print("\n=== Item 5c — interpretação de β₁ ===")
    print(f"β₁ = {b1:.4f} > 0: a probabilidade de entrega correta AUMENTA com a antecedência")
    print(f"erro padrão de β₁ : {ep[1]:.4f}   (z = {z_wald[1]:.2f})")
    print(f"IC 95% de β₁      : [{ic_b1[0]:.4f}, {ic_b1[1]:.4f}]")
    print(f"razão de chances  : e^β₁ = {razao_chance:.4f} → cada hora multiplica a chance por {razao_chance:.2f}")
    print(f"IC 95% da razão   : [{ic_rc[0]:.3f}, {ic_rc[1]:.3f}]")
    print(f"10 horas a mais   : chance × e^(10·β₁) = {np.exp(10 * b1):.1f}")
    print(f"p(x) = 0,5 em     : x = −β₀/β₁ = {x_meio:.3f} h")
    print(f"inclinação máxima : β₁/4 = {b1 / 4:.4f} por hora (em x = {x_meio:.2f} h)")
    print(f"ℓ modelo = {ell:.4f}   ℓ nulo = {ell_nulo:.4f}")
    print(f"razão de verossimilhança: D = {D:.3f}, p = {valor_p:.2e}")
    print(f"R² de McFadden: {r2_mcfadden:.3f}")

    # --- itens 5d e 5e: probabilidades -------------------------------------------
    print("\n=== Itens 5d e 5e — probabilidades ===")
    print(f"{'x (h)':>6} {'Z(x)':>8} {'chance':>8} {'P(Y=1|x)':>10} {'P(Y=0|x)':>10}")
    for h in [5, 10, 15, 20]:
        zh = b0 + b1 * h
        ph = sigmoide(zh)
        print(f"{h:>6} {zh:>8.4f} {np.exp(zh):>8.3f} {ph:>10.4f} {1 - ph:>10.4f}")

    # --- sensibilidade: o pedido mais estranho -----------------------------------
    i_estranho = int(np.argmin(np.where(y == 0, -x, np.inf)))     # o atraso de maior x
    sem = np.arange(n) != i_estranho
    beta_sem, _ = ajustar_newton(x[sem], y[sem])
    print("\n=== Sensibilidade ===")
    print(f"pedido com maior surpresa entre os atrasos: {df['pedido'].iloc[i_estranho]}, "
          f"x = {x[i_estranho]} h, p = {p[i_estranho]:.3f}")
    print(f"sem ele: β₀ = {beta_sem[0]:.4f}, β₁ = {beta_sem[1]:.4f} ({beta_sem[1] / b1 - 1:+.1%})")

    # --- figura: o caminho de cada método ----------------------------------------
    B0, B1 = np.meshgrid(np.linspace(-5.2, 0.7, 240), np.linspace(-0.04, 0.46, 240))
    Z3 = B0[..., None] + B1[..., None] * x
    ELL = np.sum(y * Z3 - np.logaddexp(0, Z3), axis=-1)

    fig, ax = plt.subplots(figsize=(8, 5.4))
    niveis = ell - np.array([40, 25, 15, 9, 5, 2.5, 1, 0.3])
    ax.contour(B0, B1, ELL, levels=np.sort(niveis), colors=COR_APOIO, linewidths=0.9, alpha=0.55,
               linestyles="solid")      # sem isso, níveis negativos saem tracejados
    ax.plot(traj_gd[:, 0], traj_gd[:, 1], color=COR_ATRASO, linewidth=2.2,
            label=f"Subida de gradiente ({iter_gd:,} passos)".replace(",", "."))
    ax.plot(traj_newton[:, 0], traj_newton[:, 1], color=COR_CORRETA, linewidth=2,
            marker="o", markersize=8, markeredgecolor="white", label=f"Newton ({iter_newton} passos)")
    ax.scatter([b0], [b1], s=170, marker="*", color=COR_MODELO, zorder=5, label="Máximo de ℓ")
    ax.set_xlabel("β₀")
    ax.set_ylabel("β₁")
    ax.grid(False)
    ax.xaxis.set_major_formatter(comum.virgula(0))
    ax.yaxis.set_major_formatter(comum.virgula(1))
    ax.set_title("Dois caminhos até o mesmo topo")
    ax.legend(loc="upper right", frameon=True, facecolor=comum.COR_SUPERFICIE, edgecolor="none",
              framealpha=0.92)
    fig.savefig(FIGURAS / "02_caminho_otimizacao.png")
    plt.close(fig)

    print(f"\nFigura salva em {FIGURAS.name}/")
