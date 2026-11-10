"""
comum.py — leitura dos dados e estilo das figuras, usados por todas as etapas.

Não tem matemática aqui: só o que os quatro scripts precisariam repetir.
"""

import importlib.util
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

AQUI = Path(__file__).parent
FIGURAS = AQUI / "figuras"
FIGURAS.mkdir(exist_ok=True)

# Cor e forma andam juntas: a classe continua legível em preto e branco
# e para quem não distingue as cores.
COR_CORRETA = "#2a78d6"   # y = 1
COR_ATRASO = "#eb6834"    # y = 0
MARCA_CORRETA = "o"
MARCA_ATRASO = "s"
COR_MODELO = "#0b0b0b"
COR_APOIO = "#52514e"
COR_GRADE = "#e4e3df"
COR_SUPERFICIE = "#fcfcfb"

plt.rcParams.update({
    "figure.facecolor": COR_SUPERFICIE,
    "axes.facecolor": COR_SUPERFICIE,
    "savefig.facecolor": COR_SUPERFICIE,
    "font.size": 13,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "axes.labelcolor": COR_APOIO,
    "axes.edgecolor": COR_GRADE,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color": COR_GRADE,
    "grid.linewidth": 0.8,
    "xtick.color": COR_APOIO,
    "ytick.color": COR_APOIO,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "legend.frameon": False,
    "savefig.dpi": 160,
    "savefig.bbox": "tight",
})


def virgula(casas=1):
    """Formatador de eixo com vírgula decimal."""
    return FuncFormatter(lambda v, _: f"{v:.{casas}f}".replace(".", ","))


def br(valor, casas=2):
    """Número com vírgula decimal, para textos dentro das figuras."""
    return f"{valor:.{casas}f}".replace(".", ",")


def carregar_dados():
    """
    Lê o CSV e devolve um DataFrame com colunas pedido, x, y.

    O arquivo começa com BOM (marca invisível do Excel) e os nomes das colunas têm
    acento, espaço e colchete. `utf-8-sig` descarta o BOM; renomear uma vez aqui
    evita escrever "Antecedência x [h]" no resto do código.
    """
    df = pd.read_csv(AQUI / "dados_logistica.csv", encoding="utf-8-sig")
    df.columns = ["pedido", "x", "y"]
    return df


def carregar_modulo(nome_arquivo):
    """Importa um script cujo nome começa com número (`import 02_ajuste` é inválido)."""
    spec = importlib.util.spec_from_file_location(nome_arquivo[:-3], AQUI / nome_arquivo)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)        # o bloco __main__ do módulo NÃO roda aqui
    return modulo
