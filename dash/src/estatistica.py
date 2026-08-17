"""
src/estatistica.py
==================
Funções estatísticas usadas na aba de análise.

Toda inferência é feita com SciPy; a regressão múltipla é resolvida por
mínimos quadrados com NumPy, com erros-padrão e valores-p calculados
explicitamente para manter a dependência do projeto enxuta.
"""

from typing import Sequence

import numpy as np
import pandas as pd
from scipy import stats


# ---------------------------------------------------------------------------
# Descritiva
# ---------------------------------------------------------------------------
def resumo_descritivo(serie: pd.Series) -> dict:
    """Medidas de posição, dispersão e forma de uma variável quantitativa."""
    x = serie.dropna().astype(float)
    q1, q2, q3 = x.quantile([0.25, 0.50, 0.75])
    moda = x.mode()
    return {
        "n": int(x.size),
        "media": float(x.mean()),
        "mediana": float(q2),
        "moda": float(moda.iloc[0]) if not moda.empty else float("nan"),
        "desvio": float(x.std(ddof=1)),
        "variancia": float(x.var(ddof=1)),
        "cv": float(x.std(ddof=1) / x.mean() * 100) if x.mean() else float("nan"),
        "minimo": float(x.min()),
        "maximo": float(x.max()),
        "q1": float(q1),
        "q3": float(q3),
        "iqr": float(q3 - q1),
        "amplitude": float(x.max() - x.min()),
        "assimetria": float(stats.skew(x)),
        "curtose": float(stats.kurtosis(x)),  # excesso de curtose (normal = 0)
        "erro_padrao": float(x.std(ddof=1) / np.sqrt(x.size)),
    }


def intervalo_confianca(serie: pd.Series, confianca: float = 0.95) -> tuple:
    """Intervalo de confiança para a média populacional (distribuição t)."""
    x = serie.dropna().astype(float)
    n = x.size
    if n < 2:
        return (float("nan"), float("nan"))
    erro = x.std(ddof=1) / np.sqrt(n)
    margem = stats.t.ppf(0.5 + confianca / 2, df=n - 1) * erro
    return (float(x.mean() - margem), float(x.mean() + margem))


def teste_normalidade(serie: pd.Series, n_amostra: int = 5000,
                      semente: int = 42) -> dict:
    """
    Teste de D'Agostino-Pearson sobre uma amostra aleatória.
    Amostramos porque, com n muito grande, qualquer desvio mínimo rejeita H0.
    """
    x = serie.dropna().astype(float)
    if x.size > n_amostra:
        x = x.sample(n_amostra, random_state=semente)
    estatistica, p = stats.normaltest(x)
    return {"estatistica": float(estatistica), "p": float(p), "n": int(x.size)}


# ---------------------------------------------------------------------------
# Comparação entre grupos
# ---------------------------------------------------------------------------
def comparar_grupos(grupos: Sequence[np.ndarray]) -> dict:
    """
    Compara k grupos independentes.
    Roda ANOVA (paramétrico) e Kruskal-Wallis (não paramétrico) e devolve
    o tamanho de efeito eta-quadrado, que a significância sozinha não informa.
    """
    grupos = [np.asarray(g, dtype=float) for g in grupos if len(g) > 1]
    if len(grupos) < 2:
        return {}

    f, p_anova = stats.f_oneway(*grupos)
    h, p_kruskal = stats.kruskal(*grupos)

    todos = np.concatenate(grupos)
    media_geral = todos.mean()
    sq_entre = sum(len(g) * (g.mean() - media_geral) ** 2 for g in grupos)
    sq_total = ((todos - media_geral) ** 2).sum()
    eta2 = sq_entre / sq_total if sq_total else float("nan")

    return {
        "f": float(f), "p_anova": float(p_anova),
        "h": float(h), "p_kruskal": float(p_kruskal),
        "eta2": float(eta2), "k": len(grupos), "n": int(todos.size),
    }


def comparar_duas_amostras(a: np.ndarray, b: np.ndarray) -> dict:
    """Teste t de Welch, Mann-Whitney U e d de Cohen para duas amostras."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.size < 2 or b.size < 2:
        return {}

    t, p_t = stats.ttest_ind(a, b, equal_var=False)
    u, p_u = stats.mannwhitneyu(a, b, alternative="two-sided")

    s = np.sqrt(((a.size - 1) * a.var(ddof=1) + (b.size - 1) * b.var(ddof=1))
                / (a.size + b.size - 2))
    d = (a.mean() - b.mean()) / s if s else float("nan")

    return {
        "t": float(t), "p_t": float(p_t),
        "u": float(u), "p_u": float(p_u),
        "d": float(d),
        "media_a": float(a.mean()), "media_b": float(b.mean()),
        "n_a": int(a.size), "n_b": int(b.size),
    }


def qui_quadrado(tabela: pd.DataFrame) -> dict:
    """Teste de independência entre duas qualitativas + V de Cramér."""
    chi2, p, gl, esperado = stats.chi2_contingency(tabela.values)
    n = tabela.values.sum()
    menor_dim = min(tabela.shape) - 1
    v = np.sqrt(chi2 / (n * menor_dim)) if n and menor_dim else float("nan")
    return {"chi2": float(chi2), "p": float(p), "gl": int(gl),
            "v_cramer": float(v), "n": int(n)}


def interpretar_p(p: float, alfa: float = 0.05) -> str:
    """Frase padrão de decisão do teste."""
    if p < alfa:
        return (f"p = {p:.2e} &lt; α = {alfa:.2f}: <b>rejeitamos H₀</b>, "
                f"a diferença observada é estatisticamente significativa.")
    return (f"p = {p:.4f} ≥ α = {alfa:.2f}: <b>não rejeitamos H₀</b>, "
            f"não há evidência suficiente de diferença.")


def classificar_eta2(eta2: float) -> str:
    """Convenção de Cohen para tamanho de efeito em ANOVA."""
    if eta2 < 0.01:
        return "desprezível"
    if eta2 < 0.06:
        return "pequeno"
    if eta2 < 0.14:
        return "médio"
    return "grande"


# ---------------------------------------------------------------------------
# Correlação e regressão
# ---------------------------------------------------------------------------
def correlacao(x: pd.Series, y: pd.Series) -> dict:
    """Correlação de Pearson (linear) e de Spearman (monotônica)."""
    base = pd.concat([x, y], axis=1).dropna()
    if len(base) < 3:
        return {}
    r, p_r = stats.pearsonr(base.iloc[:, 0], base.iloc[:, 1])
    rho, p_rho = stats.spearmanr(base.iloc[:, 0], base.iloc[:, 1])
    return {"r": float(r), "p_r": float(p_r),
            "rho": float(rho), "p_rho": float(p_rho), "n": len(base)}


def regressao_ols(X: pd.DataFrame, y: pd.Series) -> dict:
    """
    Regressão linear múltipla por mínimos quadrados ordinários.

    Devolve coeficientes, erros-padrão, estatísticas t, valores-p,
    R² e R² ajustado. O intercepto é adicionado internamente.
    """
    X = X.astype(float)
    y = np.asarray(y, dtype=float)
    nomes = ["Intercepto"] + list(X.columns)
    matriz = np.column_stack([np.ones(len(X)), X.values])

    beta, *_ = np.linalg.lstsq(matriz, y, rcond=None)
    ajustado = matriz @ beta
    residuo = y - ajustado

    n, k = matriz.shape
    gl = n - k
    sq_res = float(residuo @ residuo)
    sq_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - sq_res / sq_tot if sq_tot else float("nan")
    r2_aj = 1 - (1 - r2) * (n - 1) / gl if gl > 0 else float("nan")

    sigma2 = sq_res / gl if gl > 0 else float("nan")
    try:
        cov = sigma2 * np.linalg.pinv(matriz.T @ matriz)
        erros = np.sqrt(np.abs(np.diag(cov)))
    except np.linalg.LinAlgError:
        erros = np.full(k, np.nan)

    with np.errstate(divide="ignore", invalid="ignore"):
        t = beta / erros
    p = 2 * (1 - stats.t.cdf(np.abs(t), df=gl))

    tabela = pd.DataFrame({
        "Variável": nomes,
        "Coeficiente": beta,
        "Erro padrão": erros,
        "t": t,
        "p-valor": p,
    })

    return {"tabela": tabela, "r2": float(r2), "r2_aj": float(r2_aj),
            "n": int(n), "k": int(k - 1), "residuo": residuo,
            "ajustado": ajustado}
