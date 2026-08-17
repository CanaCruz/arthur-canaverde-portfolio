"""
src/estilo.py
=============
Identidade visual do dashboard: paleta, tipografia, CSS injetado e
template padrão dos gráficos Plotly.

Direção de arte: painel de terminal financeiro — fundo grafite, números em
fonte monoespaçada com alinhamento tabular, âmbar como única cor de destaque.
"""

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# ---------------------------------------------------------------------------
# Paleta
# ---------------------------------------------------------------------------
FUNDO = "#0D1117"
SUPERFICIE = "#151B23"
LINHA = "#26303B"
TEXTO = "#E8EDF2"
SUAVE = "#8A97A6"

AMBAR = "#FFB020"      # destaque principal
TEAL = "#3FB8AF"       # série secundária
VIOLETA = "#8B7BFF"    # série terciária
CORAL = "#E5674B"      # alerta / contraste
SEQUENCIA = [AMBAR, TEAL, VIOLETA, CORAL, "#5C93D6", SUAVE]

FONTE_DISPLAY = "'Space Grotesk', sans-serif"
FONTE_TEXTO = "'Inter', sans-serif"
FONTE_DADOS = "'JetBrains Mono', monospace"


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
def aplicar_estilo() -> None:
    """Injeta as fontes e o CSS do dashboard. Chamar uma vez, no app.py."""
    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {{ font-family: {FONTE_TEXTO}; }}

.stApp {{ background: {FUNDO}; }}

/* Títulos ------------------------------------------------------------- */
h1, h2, h3 {{
    font-family: {FONTE_DISPLAY};
    letter-spacing: -0.02em;
    color: {TEXTO};
}}
h1 {{ font-size: 2.5rem; font-weight: 700; line-height: 1.1; }}
h2 {{ font-size: 1.45rem; font-weight: 600; margin-top: 0.4rem; }}

/* Eyebrow numerado: usado só nas seções da análise, que são sequenciais */
.eyebrow {{
    font-family: {FONTE_DADOS};
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {AMBAR};
    display: flex; align-items: center; gap: 0.75rem;
    margin: 2.2rem 0 0.4rem 0;
}}
.eyebrow::after {{
    content: ""; flex: 1; height: 1px; background: {LINHA};
}}

.legenda {{ color: {SUAVE}; font-size: 0.9rem; line-height: 1.6; }}

/* Cartão de indicador -------------------------------------------------- */
.kpi {{
    background: {SUPERFICIE};
    border: 1px solid {LINHA};
    border-radius: 10px;
    padding: 1rem 1.1rem;
    height: 100%;
}}
.kpi-rotulo {{
    font-family: {FONTE_DADOS};
    font-size: 0.68rem; letter-spacing: 0.12em; text-transform: uppercase;
    color: {SUAVE};
}}
.kpi-valor {{
    font-family: {FONTE_DADOS};
    font-variant-numeric: tabular-nums;
    font-size: 1.6rem; font-weight: 600; color: {TEXTO};
    margin: 0.35rem 0 0.1rem 0; line-height: 1.1;
}}
.kpi-nota {{ font-size: 0.78rem; color: {SUAVE}; }}
.kpi-destaque .kpi-valor {{ color: {AMBAR}; }}

/* Caixa de leitura / insight ------------------------------------------ */
.insight {{
    background: rgba(255,176,32,0.06);
    border-left: 3px solid {AMBAR};
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.1rem;
    margin: 0.9rem 0 0.4rem 0;
    font-size: 0.92rem; line-height: 1.65; color: {TEXTO};
}}
.insight b {{ color: {AMBAR}; }}

.painel {{
    background: {SUPERFICIE};
    border: 1px solid {LINHA};
    border-radius: 10px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 0.9rem;
}}
.painel h4 {{
    font-family: {FONTE_DISPLAY}; font-size: 1rem; color: {TEXTO};
    margin: 0 0 0.15rem 0;
}}
.painel .meta {{
    font-family: {FONTE_DADOS}; font-size: 0.74rem; color: {AMBAR};
    letter-spacing: 0.06em; margin-bottom: 0.5rem;
}}
.painel p {{ color: {SUAVE}; font-size: 0.9rem; margin: 0.3rem 0; line-height: 1.6; }}
.painel ul {{ color: {SUAVE}; font-size: 0.9rem; margin: 0.4rem 0 0 1rem; line-height: 1.7; }}

/* Etiquetas de stack --------------------------------------------------- */
.tag {{
    display: inline-block;
    font-family: {FONTE_DADOS}; font-size: 0.72rem;
    color: {TEAL}; border: 1px solid rgba(63,184,175,0.35);
    background: rgba(63,184,175,0.08);
    border-radius: 4px; padding: 0.15rem 0.5rem; margin: 0.15rem 0.25rem 0.15rem 0;
}}

/* Barra de nível ------------------------------------------------------- */
.skill-linha {{ margin-bottom: 0.7rem; }}
.skill-topo {{
    display: flex; justify-content: space-between;
    font-size: 0.85rem; color: {TEXTO}; margin-bottom: 0.28rem;
}}
.skill-topo span:last-child {{
    font-family: {FONTE_DADOS}; font-variant-numeric: tabular-nums; color: {SUAVE};
}}
.skill-trilho {{ background: {LINHA}; border-radius: 3px; height: 6px; overflow: hidden; }}
.skill-barra {{ background: {AMBAR}; height: 6px; border-radius: 3px; }}

/* Ajustes de componentes nativos --------------------------------------- */
[data-testid="stSidebar"] {{ background: {SUPERFICIE}; border-right: 1px solid {LINHA}; }}
[data-testid="stMetricValue"] {{ font-family: {FONTE_DADOS}; }}
.stTabs [data-baseweb="tab"] {{
    font-family: {FONTE_DADOS}; font-size: 0.8rem; letter-spacing: 0.04em;
}}
.stDataFrame {{ border: 1px solid {LINHA}; border-radius: 8px; }}
hr {{ border-color: {LINHA}; }}
footer, #MainMenu {{ visibility: hidden; }}
</style>
""",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Template Plotly
# ---------------------------------------------------------------------------
def registrar_template() -> None:
    """Registra e ativa o template Plotly com a identidade do dashboard."""
    pio.templates["painel"] = go.layout.Template(
        layout=go.Layout(
            font=dict(family="Inter, sans-serif", color=TEXTO, size=13),
            title=dict(font=dict(family="Space Grotesk, sans-serif", size=16)),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            colorway=SEQUENCIA,
            xaxis=dict(gridcolor=LINHA, zerolinecolor=LINHA, linecolor=LINHA,
                       tickfont=dict(family="JetBrains Mono, monospace", size=11,
                                     color=SUAVE)),
            yaxis=dict(gridcolor=LINHA, zerolinecolor=LINHA, linecolor=LINHA,
                       tickfont=dict(family="JetBrains Mono, monospace", size=11,
                                     color=SUAVE)),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11, color=SUAVE)),
            margin=dict(l=10, r=10, t=48, b=10),
            hoverlabel=dict(bgcolor=SUPERFICIE, bordercolor=LINHA,
                            font=dict(family="JetBrains Mono, monospace", size=12)),
        )
    )
    pio.templates.default = "painel"
