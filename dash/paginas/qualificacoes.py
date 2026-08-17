"""
paginas/qualificacoes.py
========================
Aba 2 — formação, cursos, experiências e idiomas. Conteúdo vindo de perfil.py.
"""

from pathlib import Path

import streamlit as st

import perfil
from src import componentes as ui


def _arquivo_asset(relativo: str) -> Path | None:
    if not relativo:
        return None
    bases = [
        Path(perfil.__file__).resolve().parent,
        Path.cwd() / "dash",
        Path.cwd(),
    ]
    for base in bases:
        caminho = (base / relativo).resolve()
        if caminho.is_file():
            return caminho
    return None


def render() -> None:
    ui.cabecalho(
        "Minhas qualificações",
        "Formação acadêmica, certificações, experiências e idiomas.",
    )

    esquerda, direita = st.columns([1.35, 1], gap="large")

    with esquerda:
        ui.secao("01", "Formação acadêmica")
        for item in perfil.FORMACAO:
            ui.painel(
                titulo=item["curso"],
                meta=f"{item['instituicao']} · {item['periodo']}",
                texto=item.get("detalhe", ""),
            )

        ui.secao("02", "Experiência e projetos")
        for item in perfil.EXPERIENCIAS:
            ui.painel(
                titulo=item["cargo"],
                meta=f"{item['empresa']} · {item['periodo']}",
                itens=item.get("atividades", []),
            )

    with direita:
        ui.secao("03", "Cursos e certificações")
        for item in perfil.CURSOS:
            ui.painel(
                titulo=item["nome"],
                meta=f"{item['emissor']} · {item['ano']}",
            )
            caminho = _arquivo_asset(item.get("arquivo", ""))
            if caminho is not None:
                st.download_button(
                    label="Baixar certificado PDF",
                    data=caminho.read_bytes(),
                    file_name=caminho.name,
                    mime="application/pdf",
                    key=f"cert_{caminho.stem}",
                )

        ui.secao("04", "Idiomas")
        st.markdown("<div class='painel'>", unsafe_allow_html=True)
        for item in perfil.IDIOMAS:
            ui.barra_nivel(f"{item['idioma']} — {item['nivel']}", item["escala"])
        st.markdown("</div>", unsafe_allow_html=True)
