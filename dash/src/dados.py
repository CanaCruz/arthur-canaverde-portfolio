"""
src/dados.py
============
Carregamento, tratamento e enriquecimento da base de dados.

Fonte: ai-jobs.net Global Salaries in AI, ML & Data Science
       (https://ai-jobs.net/salaries/ — domínio público, CC0).
Arquivo local: data/salaries.csv

A base reúne autodeclarações de remuneração anual bruta em cargos de
tecnologia, dados e IA entre 2020 e 2025, com país da empresa, país de
residência, senioridade, regime de trabalho e porte da organização.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

CAMINHO_BASE = Path(__file__).resolve().parent.parent / "data" / "salaries.csv"

# ---------------------------------------------------------------------------
# Dicionários de tradução dos códigos da base
# ---------------------------------------------------------------------------
SENIORIDADE = {
    "EN": "Júnior",
    "MI": "Pleno",
    "SE": "Sênior",
    "EX": "Executivo",
}
ORDEM_SENIORIDADE = ["Júnior", "Pleno", "Sênior", "Executivo"]

CONTRATO = {
    "FT": "Tempo integral",
    "PT": "Meio período",
    "CT": "Contrato/PJ",
    "FL": "Freelancer",
}

REGIME = {0: "Presencial", 50: "Híbrido", 100: "Remoto"}
ORDEM_REGIME = ["Presencial", "Híbrido", "Remoto"]

PORTE = {"S": "Pequena", "M": "Média", "L": "Grande"}
ORDEM_PORTE = ["Pequena", "Média", "Grande"]

PAISES = {
    "US": "Estados Unidos", "CA": "Canadá", "GB": "Reino Unido", "DE": "Alemanha",
    "FR": "França", "ES": "Espanha", "NL": "Países Baixos", "AU": "Austrália",
    "IN": "Índia", "BR": "Brasil", "PT": "Portugal", "IT": "Itália",
    "PL": "Polônia", "MX": "México", "AR": "Argentina", "CO": "Colômbia",
    "CL": "Chile", "JP": "Japão", "SG": "Singapura", "IE": "Irlanda",
    "CH": "Suíça", "SE": "Suécia", "NO": "Noruega", "DK": "Dinamarca",
    "FI": "Finlândia", "BE": "Bélgica", "AT": "Áustria", "GR": "Grécia",
    "TR": "Turquia", "IL": "Israel", "AE": "Emirados Árabes", "ZA": "África do Sul",
    "NG": "Nigéria", "KE": "Quênia", "CN": "China", "KR": "Coreia do Sul",
    "NZ": "Nova Zelândia", "RO": "Romênia", "CZ": "Tchéquia", "HU": "Hungria",
    "UA": "Ucrânia", "RU": "Rússia", "LT": "Lituânia", "LV": "Letônia",
    "EE": "Estônia", "HR": "Croácia", "SI": "Eslovênia", "SK": "Eslováquia",
    "BG": "Bulgária", "RS": "Sérvia", "LU": "Luxemburgo", "MT": "Malta",
    "CY": "Chipre", "IS": "Islândia", "PH": "Filipinas", "VN": "Vietnã",
    "TH": "Tailândia", "MY": "Malásia", "ID": "Indonésia", "PK": "Paquistão",
    "EG": "Egito", "SA": "Arábia Saudita", "QA": "Catar", "HK": "Hong Kong",
    "PR": "Porto Rico", "DZ": "Argélia", "GH": "Gana", "AM": "Armênia",
    "BA": "Bósnia", "MD": "Moldávia", "AD": "Andorra", "AS": "Samoa Americana",
}

# Famílias de cargo — agrupa 400+ títulos livres em categorias analisáveis.
FAMILIAS = [
    ("Engenharia de Software", ["software engineer", "software developer",
                                "backend", "back end", "frontend", "front end",
                                "full stack", "fullstack", "web developer",
                                "mobile", "devops", "sre", "platform engineer",
                                "cloud engineer", "qa ", "test engineer"]),
    ("Engenharia de Dados", ["data engineer", "analytics engineer", "etl",
                             "big data", "data infrastructure", "data ops",
                             "database", "data architect", "data governance",
                             "data quality", "data management", "data modeler",
                             "data specialist", "data developer", "data steward"]),
    ("Ciência de Dados", ["data scientist", "research scientist",
                          "applied scientist", "decision scientist",
                          "data science"]),
    ("IA e Machine Learning", ["machine learning", "ml engineer", "ai engineer",
                               "deep learning", "nlp", "computer vision",
                               "ai scientist", "ai research", "mlops",
                               " ai ", "artificial intelligence", "llm"]),
    ("Análise de Dados / BI", ["data analyst", "business intelligence", "bi ",
                               "analytics", "insight analyst", "reporting"]),
    ("Gestão e Produto", ["manager", "head", "director", "lead", "chief",
                          "vp ", "product owner", "product manager", "scrum"]),
]


# Segunda passada: termos genéricos, aplicados só quando a primeira não casa.
# Títulos como "Engineer" ou "Analyst" aparecem sozinhos milhares de vezes.
GENERICOS = [
    ("Análise de Dados / BI", ["analyst", "analytics"]),
    ("Ciência de Dados", ["scientist", "research"]),
    ("Engenharia de Software", ["engineer", "developer", "architect",
                                "technical staff", "programmer"]),
]


def _familia_do_cargo(titulo: str) -> str:
    """
    Classifica um título de cargo em uma família ocupacional.

    A base traz 422 títulos em texto livre. A classificação é feita em duas
    passadas: primeiro termos compostos e específicos ('data engineer'),
    depois termos genéricos ('engineer'), o que evita que 'Data Engineer'
    caia na família errada por causa da palavra 'engineer'.
    """
    t = f" {titulo.lower()} "
    for familia, chaves in FAMILIAS:
        if any(chave in t for chave in chaves):
            return familia
    for familia, chaves in GENERICOS:
        if any(chave in t for chave in chaves):
            return familia
    return "Outros"


@st.cache_data(show_spinner="Carregando base de dados...")
def carregar_dados() -> pd.DataFrame:
    """
    Lê o CSV bruto e devolve o DataFrame tratado.

    Etapas de tratamento (documentadas na aba 01 do dashboard):
      1. leitura com tipagem explícita;
      2. tradução dos códigos categóricos para rótulos legíveis;
      3. criação da variável 'familia_cargo' a partir do título livre;
      4. criação de variáveis ordinais e do log do salário;
      5. marcação (não remoção) de outliers pelo critério de Tukey.
    """
    df = pd.read_csv(CAMINHO_BASE)

    df = df.rename(columns={
        "work_year": "ano",
        "experience_level": "senioridade_cod",
        "employment_type": "contrato_cod",
        "job_title": "cargo",
        "salary": "salario_local",
        "salary_currency": "moeda",
        "salary_in_usd": "salario_usd",
        "employee_residence": "residencia_cod",
        "remote_ratio": "remoto_pct",
        "company_location": "pais_cod",
        "company_size": "porte_cod",
    })

    # 2. Rótulos legíveis --------------------------------------------------
    df["senioridade"] = df["senioridade_cod"].map(SENIORIDADE)
    df["contrato"] = df["contrato_cod"].map(CONTRATO)
    df["regime"] = df["remoto_pct"].map(REGIME)
    df["porte"] = df["porte_cod"].map(PORTE)
    df["pais"] = df["pais_cod"].map(PAISES).fillna(df["pais_cod"])
    df["residencia"] = df["residencia_cod"].map(PAISES).fillna(df["residencia_cod"])

    # 3. Família ocupacional ----------------------------------------------
    mapa = {t: _familia_do_cargo(t) for t in df["cargo"].unique()}
    df["familia_cargo"] = df["cargo"].map(mapa)

    # 4. Variáveis derivadas ----------------------------------------------
    df["senioridade"] = pd.Categorical(df["senioridade"],
                                       categories=ORDEM_SENIORIDADE, ordered=True)
    df["regime"] = pd.Categorical(df["regime"], categories=ORDEM_REGIME, ordered=True)
    df["porte"] = pd.Categorical(df["porte"], categories=ORDEM_PORTE, ordered=True)
    df["senioridade_num"] = df["senioridade"].cat.codes  # 0..3 — variável ordinal
    df["log_salario"] = np.log(df["salario_usd"])
    df["mesmo_pais"] = np.where(df["pais_cod"] == df["residencia_cod"],
                                "Mesmo país", "Contratação internacional")

    # 5. Outliers pelo critério de Tukey (marcados, não excluídos) ---------
    q1, q3 = df["salario_usd"].quantile([0.25, 0.75])
    iqr = q3 - q1
    limite_inf, limite_sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    df["outlier"] = (df["salario_usd"] < limite_inf) | (df["salario_usd"] > limite_sup)

    return df


def aplicar_filtros(df: pd.DataFrame, anos, paises, familias,
                    senioridades, sem_outliers: bool) -> pd.DataFrame:
    """Aplica os filtros da barra lateral. Listas vazias significam 'tudo'."""
    recorte = df[df["ano"].between(anos[0], anos[1])]
    if paises:
        recorte = recorte[recorte["pais"].isin(paises)]
    if familias:
        recorte = recorte[recorte["familia_cargo"].isin(familias)]
    if senioridades:
        recorte = recorte[recorte["senioridade"].isin(senioridades)]
    if sem_outliers:
        recorte = recorte[~recorte["outlier"]]
    return recorte


DICIONARIO = pd.DataFrame([
    ("ano", "Quantitativa discreta", "Ano de referência do salário (2020–2025)"),
    ("cargo", "Qualitativa nominal", "Título do cargo, texto livre (422 valores)"),
    ("familia_cargo", "Qualitativa nominal", "Família ocupacional derivada do título"),
    ("senioridade", "Qualitativa ordinal", "Júnior < Pleno < Sênior < Executivo"),
    ("contrato", "Qualitativa nominal", "Integral, meio período, PJ ou freelancer"),
    ("regime", "Qualitativa ordinal", "Presencial < Híbrido < Remoto"),
    ("porte", "Qualitativa ordinal", "Pequena < Média < Grande"),
    ("pais", "Qualitativa nominal", "País da sede da empresa"),
    ("residencia", "Qualitativa nominal", "País de residência do profissional"),
    ("salario_local", "Quantitativa contínua", "Remuneração anual na moeda de origem"),
    ("salario_usd", "Quantitativa contínua", "Remuneração anual bruta em dólares"),
    ("log_salario", "Quantitativa contínua", "Log natural do salário (derivada)"),
    ("outlier", "Qualitativa binária", "Marcação pelo critério de Tukey (1,5·IQR)"),
], columns=["Variável", "Tipo", "Descrição"])
