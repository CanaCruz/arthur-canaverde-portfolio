"""
app.py
======
Dashboard Profissional com Análise de Dados
CP1 — Data Science and Statistical Computing — FIAP

Ponto de entrada da aplicação. Configura a página, aplica a identidade
visual e registra a navegação entre as quatro abas exigidas no enunciado.

Execução local:
    streamlit run app.py
"""

import streamlit as st

import perfil
from paginas import analise, qualificacoes, quem_sou_eu, skills
from src.estilo import aplicar_estilo, registrar_template

st.set_page_config(
    page_title=f"{perfil.PERFIL['nome']} - Dashboard Profissional",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

aplicar_estilo()
registrar_template()

# --- Cabeçalho fixo da barra lateral ---------------------------------------
st.sidebar.markdown(
    f"<div style='padding:0.2rem 0 1rem 0'>"
    f"<div style='font-family:JetBrains Mono,monospace;font-size:0.68rem;"
    f"letter-spacing:0.16em;text-transform:uppercase;color:#FFB020'>"
    f"Dashboard profissional</div>"
    f"<div style='font-family:Space Grotesk,sans-serif;font-size:1.05rem;"
    f"color:#E8EDF2;margin-top:0.2rem'>{perfil.PERFIL['nome']}</div>"
    f"<div style='font-size:0.78rem;color:#8A97A6'>{perfil.PERFIL['cargo_alvo']}</div>"
    f"</div><hr style='margin:0 0 0.5rem 0'>",
    unsafe_allow_html=True,
)

# --- Navegação --------------------------------------------------------------
paginas = [
    st.Page(quem_sou_eu.render, title="Quem sou eu", icon=":material/person:",
            url_path="quem-sou-eu", default=True),
    st.Page(qualificacoes.render, title="Minhas qualificações",
            icon=":material/school:", url_path="qualificacoes"),
    st.Page(skills.render, title="Skills", icon=":material/bolt:",
            url_path="skills"),
    st.Page(analise.render, title="Análise de Dados",
            icon=":material/insights:", url_path="analise"),
]

st.navigation(paginas).run()

# --- Rodapé -----------------------------------------------------------------
st.sidebar.markdown(
    "<hr><p style='font-size:0.72rem;color:#8A97A6;line-height:1.5'>"
    "Construído em Python com Streamlit, Pandas, SciPy e Plotly.<br>"
    "Base: ai-jobs.net Global Salaries (CC0).</p>",
    unsafe_allow_html=True,
)
