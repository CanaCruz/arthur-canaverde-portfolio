"""
paginas/skills.py
=================
Aba 3 — competências técnicas (barras), visão geral (radar), soft skills
e projetos. Conteúdo vindo de perfil.py.
"""

import plotly.graph_objects as go
import streamlit as st

import perfil
from src import componentes as ui
from src.estilo import AMBAR, LINHA, SUAVE


def _radar() -> go.Figure:
    eixos = list(perfil.RADAR.keys())
    valores = list(perfil.RADAR.values())
    # Fecha o polígono repetindo o primeiro ponto.
    eixos_fechados = eixos + [eixos[0]]
    valores_fechados = valores + [valores[0]]

    figura = go.Figure(
        go.Scatterpolar(
            r=valores_fechados,
            theta=eixos_fechados,
            fill="toself",
            fillcolor="rgba(255,176,32,0.16)",
            line=dict(color=AMBAR, width=2),
            hovertemplate="%{theta}: %{r}<extra></extra>",
        )
    )
    figura.update_layout(
        height=380,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=LINHA,
                            tickfont=dict(size=10, color=SUAVE), showline=False),
            angularaxis=dict(gridcolor=LINHA,
                             tickfont=dict(family="JetBrains Mono, monospace",
                                           size=11, color=SUAVE)),
        ),
        showlegend=False,
        margin=dict(l=60, r=60, t=30, b=30),
    )
    return figura


def render() -> None:
    ui.cabecalho(
        "Skills",
        "Competências técnicas, ferramentas e habilidades interpessoais. "
        "Os níveis seguem uma escala de autoavaliação de 0 a 100.",
    )

    esquerda, direita = st.columns([1.3, 1], gap="large")

    with esquerda:
        ui.secao("01", "Competências técnicas")
        for grupo, habilidades in perfil.SKILLS_TECNICAS.items():
            st.markdown(
                f"<div class='painel'><div class='meta'>{grupo}</div>",
                unsafe_allow_html=True,
            )
            for habilidade in habilidades:
                ui.barra_nivel(habilidade["nome"], habilidade["nivel"])
            st.markdown("</div>", unsafe_allow_html=True)

    with direita:
        ui.secao("02", "Visão geral")
        st.plotly_chart(_radar(), width="stretch",
                        config={"displayModeBar": False})

        ui.secao("03", "Soft skills")
        for item in perfil.SOFT_SKILLS:
            ui.painel(titulo=item["nome"], texto=item["descricao"])

    ui.secao("04", "Projetos")
    colunas = st.columns(min(len(perfil.PROJETOS), 3), gap="medium")
    for coluna, projeto in zip(colunas, perfil.PROJETOS):
        with coluna:
            titulo = projeto["titulo"]
            if projeto.get("link"):
                titulo = (f"<a href='{projeto['link']}' target='_blank' "
                          f"style='color:inherit;text-decoration:none'>{titulo} ↗</a>")
            ui.painel(
                titulo=titulo,
                texto=projeto["descricao"],
                tags=projeto.get("stack", []),
            )
