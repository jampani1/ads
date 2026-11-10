"""
04_metricas.py — Item 8: calcular e interpretar as métricas
Atividade de IC: Classificação de entregas por Regressão Logística.

===============================================================================
MATEMÁTICA DA ETAPA — cada métrica é uma pergunta diferente
===============================================================================

Classe positiva = entrega na data correta. Da matriz de confusão:

    Acurácia       = (VP + VN) / n      de todos os pedidos, quantos acertei?
    Precisão       = VP / (VP + FP)     dos que previ corretos, quantos eram?
    Recall         = VP / (VP + FN)     dos que eram corretos, quantos achei?
    Especificidade = VN / (VN + FP)     dos atrasos, quantos achei?
    F1             = 2·P·R / (P + R)    média harmônica de precisão e recall

Observação: o enunciado escreve "Previsão da classe positiva"; a fórmula usada aqui é
a da PRECISÃO (valor preditivo positivo), a única da lista com esse papel.

F1 usa a média HARMÔNICA porque ela é puxada para o menor dos dois valores: um
classificador só tem F1 alto se precisão E recall forem altos. Substituindo P e R:

    F1 = 2·VP / (2·VP + FP + FN)

Essa forma mostra o que F1 ignora: VN não aparece. Ele não enxerga os atrasos
identificados, e por isso a especificidade precisa vir ao lado.

CURVA ROC (extra, está no cronograma da IC). Para cada limiar t, marca-se
(1 − especificidade, recall). A área sob a curva tem uma leitura exata:

    AUC = P( p de um pedido correto > p de um pedido atrasado )

É a estatística U de Mann-Whitney dividida por n₁·n₀. A AUC não depende de limiar: ela
avalia o ORDENAMENTO que o modelo produz, e a verificação abaixo confere essa identidade.

INCERTEZA. Acurácia é uma proporção de n = 42 tentativas. O intervalo de Wilson é
adequado a n pequeno:

    centro = (p̂ + z²/2n) / (1 + z²/n)
    raio   = z·√( p̂(1−p̂)/n + z²/4n² ) / (1 + z²/n)

E ela foi medida nos mesmos pedidos usados para ajustar o modelo e escolher o limiar,
portanto é otimista. A validação leave-one-out corrige isso: tira um pedido, refaz TUDO
(β e limiar) com os outros 41 e prevê o que ficou de fora. Repete 42 vezes.

===============================================================================
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

import comum
from comum import COR_APOIO, COR_CORRETA, COR_MODELO, FIGURAS, br

ajuste = comum.carregar_modulo("02_ajuste.py")
classif = comum.carregar_modulo("03_classificacao.py")

x, y, df = ajuste.x, ajuste.y, ajuste.df
n = len(y)
beta, p, LIMIAR, y_hat = classif.beta, classif.p, classif.LIMIAR, classif.y_hat


def metricas(y, y_hat):
    """Devolve um dicionário com as cinco métricas do enunciado."""
    vn, fp, fn, vp = classif.matriz_confusao(y, y_hat)
    precisao = vp / (vp + fp)
    recall = vp / (vp + fn)
    return {
        "Acurácia": (vp + vn) / len(y),
        "Precisão": precisao,
        "Recall": recall,
        "Especificidade": vn / (vn + fp),
        "F1": 2 * precisao * recall / (precisao + recall),
    }


def wilson(acertos, total, confianca=0.95):
    """Intervalo de Wilson para uma proporção."""
    z = stats.norm.ppf(0.5 + confianca / 2)
    phat = acertos / total
    denominador = 1 + z ** 2 / total
    centro = (phat + z ** 2 / (2 * total)) / denominador
    raio = z * np.sqrt(phat * (1 - phat) / total + z ** 2 / (4 * total ** 2)) / denominador
    return centro - raio, centro + raio


def curva_roc(p, y):
    """Pontos (1 − especificidade, recall), do limiar mais alto ao mais baixo."""
    limiares = np.r_[np.inf, np.sort(np.unique(p))[::-1]]
    fpr = np.array([((p >= t) & (y == 0)).sum() / (y == 0).sum() for t in limiares])
    tpr = np.array([((p >= t) & (y == 1)).sum() / (y == 1).sum() for t in limiares])
    return fpr, tpr


def area_trapezios(fpr, tpr):
    """Integral de tpr em fpr pela regra do trapézio."""
    return float(np.sum(np.diff(fpr) * (tpr[1:] + tpr[:-1]) / 2))


def auc_por_pares(p, y):
    """Fração de pares (correto, atrasado) em que o correto recebeu p maior."""
    corretos, atrasos = p[y == 1], p[y == 0]
    diferencas = corretos[:, None] - atrasos[None, :]
    return float(((diferencas > 0).sum() + 0.5 * (diferencas == 0).sum()) / diferencas.size)


def leave_one_out(x, y):
    """Refaz ajuste e limiar sem cada pedido. Devolve as previsões fora da amostra."""
    previsto_otimo = np.zeros(len(y), dtype=int)
    previsto_05 = np.zeros(len(y), dtype=int)
    for i in range(len(y)):
        fora = np.arange(len(y)) != i
        b, _ = ajuste.ajustar_newton(x[fora], y[fora])
        p_treino = ajuste.prever_p(x[fora], b)
        candidatos, acertos = classif.varrer_limiares(p_treino, y[fora])
        k = int(np.argmax(acertos))              # em empate, fica com o primeiro degrau
        inferior = candidatos[k - 1] if k > 0 else 0.0
        t = (inferior + candidatos[k]) / 2
        p_i = ajuste.prever_p(x[i], b)
        previsto_otimo[i] = int(p_i >= t)
        previsto_05[i] = int(p_i >= 0.5)
    return previsto_otimo, previsto_05


if __name__ == "__main__":
    vn, fp, fn, vp = classif.matriz_confusao(y, y_hat)
    m = metricas(y, y_hat)
    m05 = metricas(y, classif.classificar(p, 0.5))

    print("=== Item 8 — métricas ===")
    print(f"VN = {vn}, FP = {fp}, FN = {fn}, VP = {vp}\n")
    print(f"{'':>16}{'t*':>10}{'t = 0,5':>10}")
    for nome in m:
        print(f"{nome:>16}{m[nome]:>10.4f}{m05[nome]:>10.4f}")

    # --- verificações --------------------------------------------------------------
    assert np.isclose(m["F1"], 2 * vp / (2 * vp + fp + fn))
    assert np.isclose(m["Acurácia"],
                      (m["Recall"] * y.sum() + m["Especificidade"] * (n - y.sum())) / n)
    print("\nconferido: F1 = 2VP/(2VP+FP+FN)")
    print("conferido: acurácia = média de recall e especificidade, ponderada pelo tamanho das classes")
    try:
        from sklearn import metrics as sk
        assert np.isclose(m["Acurácia"], sk.accuracy_score(y, y_hat))
        assert np.isclose(m["Precisão"], sk.precision_score(y, y_hat))
        assert np.isclose(m["Recall"], sk.recall_score(y, y_hat))
        assert np.isclose(m["Especificidade"], sk.recall_score(y, y_hat, pos_label=0))
        assert np.isclose(m["F1"], sk.f1_score(y, y_hat))
        print("conferido: as cinco métricas batem com sklearn.metrics")
    except ImportError:
        sk = None
        print("scikit-learn indisponível: conferência pulada")

    # --- referência ----------------------------------------------------------------
    print("\n=== Comparação com o modelo que não olha x ===")
    base = max(y.mean(), 1 - y.mean())
    print(f"sempre prever a classe mais comum: acurácia {base:.4f} ({int(base * n)}/{n})")
    print(f"ganho do modelo: {m['Acurácia'] - base:+.4f}")

    ic = wilson(round(m["Acurácia"] * n), n)
    print(f"\nIC 95% de Wilson para a acurácia: [{ic[0]:.3f}, {ic[1]:.3f}]")

    # --- leave-one-out -------------------------------------------------------------
    loo_otimo, loo_05 = leave_one_out(x, y)
    print("\n=== Leave-one-out (refazendo β e limiar a cada rodada) ===")
    print(f"{'':>16}{'limiar otimizado':>18}{'t = 0,5':>10}")
    a, b = metricas(y, loo_otimo), metricas(y, loo_05)
    for nome in a:
        print(f"{nome:>16}{a[nome]:>18.4f}{b[nome]:>10.4f}")
    print(f"acertos: {(loo_otimo == y).sum()}/{n} com limiar otimizado, {(loo_05 == y).sum()}/{n} com t = 0,5")

    # --- ROC -----------------------------------------------------------------------
    fpr, tpr = curva_roc(p, y)
    auc_trap = area_trapezios(fpr, tpr)
    auc_pares = auc_por_pares(p, y)
    u = stats.mannwhitneyu(p[y == 1], p[y == 0]).statistic
    auc_mw = u / (y.sum() * (n - y.sum()))
    print("\n=== ROC ===")
    print(f"AUC por trapézios   : {auc_trap:.6f}")
    print(f"AUC por pares       : {auc_pares:.6f}")
    print(f"AUC por Mann-Whitney: {auc_mw:.6f}")
    assert np.isclose(auc_trap, auc_pares) and np.isclose(auc_pares, auc_mw)
    if sk is not None:
        assert np.isclose(auc_trap, sk.roc_auc_score(y, p))
        print("conferido: as três formas e sklearn.metrics.roc_auc_score coincidem")

    # --- calibração ----------------------------------------------------------------
    # Compara, em cada faixa, a soma das probabilidades com o número de entregas corretas.
    # A equação de escore garante que os totais batem; as faixas mostram onde o modelo erra.
    print("\n=== Calibração por faixa ===")
    print(f"{'faixa':>10}{'n':>5}{'previstas':>11}{'observadas':>12}{'p médio':>9}{'taxa':>7}")
    bordas = [0, 6, 12, 18, 24]
    for a_h, b_h in zip(bordas[:-1], bordas[1:]):
        sel = (x >= a_h) & (x < b_h)
        print(f"{f'{a_h}–{b_h} h':>10}{sel.sum():>5}{p[sel].sum():>11.2f}{y[sel].sum():>12}"
              f"{p[sel].mean():>9.3f}{y[sel].mean():>7.3f}")
    assert np.isclose(p.sum(), y.sum())

    # --- decisão -------------------------------------------------------------------
    print("\n=== Antecedência mínima para cada meta de confiança ===")
    print(f"{'meta p(x)':>10}{'x (h)':>10}{'pedidos com x ≥':>18}{'taxa observada':>17}")
    for meta in [0.5, 0.7, 0.8, 0.9, 0.95]:
        minimo = classif.inverter(meta, beta)
        sel = x >= minimo
        observada = y[sel].mean() if sel.any() else float("nan")
        print(f"{meta:>10.2f}{minimo:>10.2f}{sel.sum():>18}{observada:>17.3f}")

    # A acurácia conta um FP e um FN como o mesmo erro. Se prometer no prazo e atrasar
    # custa mais, o limiar sobe: troca-se recall por especificidade.
    print("\n=== O que acontece ao subir o limiar ===")
    print(f"{'t':>7}{'x (h)':>8}{'VN':>4}{'FP':>4}{'FN':>4}{'VP':>4}{'acur.':>8}{'prec.':>8}{'recall':>8}{'espec.':>8}")
    for t in [LIMIAR, 0.7, 0.8, 0.9]:
        previsto = classif.classificar(p, t)
        c = classif.matriz_confusao(y, previsto)
        r = metricas(y, previsto)
        print(f"{t:>7.3f}{classif.inverter(t, beta):>8.2f}{c[0]:>4}{c[1]:>4}{c[2]:>4}{c[3]:>4}"
              f"{r['Acurácia']:>8.3f}{r['Precisão']:>8.3f}{r['Recall']:>8.3f}{r['Especificidade']:>8.3f}")

    # --- figura: ROC ---------------------------------------------------------------
    corte_fpr = fp / (fp + vn)
    corte_tpr = vp / (vp + fn)
    fig, ax = plt.subplots(figsize=(6.2, 6))
    ax.plot([0, 1], [0, 1], color=COR_APOIO, linewidth=1.2, linestyle=":", label="Sem poder de separação")
    ax.step(fpr, tpr, where="post", color=COR_CORRETA, linewidth=2.2, label=f"Modelo (AUC = {br(auc_trap, 3)})")
    ax.scatter([corte_fpr], [corte_tpr], s=110, color=COR_MODELO, zorder=4, label="Limiar t*")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.set_aspect("equal")
    ax.xaxis.set_major_formatter(comum.virgula(1))
    ax.yaxis.set_major_formatter(comum.virgula(1))
    ax.set_xlabel("1 − especificidade (atrasos não detectados)")
    ax.set_ylabel("Recall (entregas corretas detectadas)")
    ax.set_title("Curva ROC")
    ax.legend(loc="lower right")
    fig.savefig(FIGURAS / "04_roc.png")
    plt.close(fig)

    print(f"\nFigura salva em {FIGURAS.name}/")
