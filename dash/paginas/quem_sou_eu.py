"""
paginas/quem_sou_eu.py
======================
Aba 1 — apresentação profissional. Todo o conteúdo vem de perfil.py.
"""

from pathlib import Path

import streamlit as st

import perfil
from src import componentes as ui
from src.estilo import AMBAR, SUAVE


def _arquivo_asset(relativo: str) -> Path | None:
    """Resolve assets/… tanto no Cloud (cwd = raiz do repo) quanto local."""
    if not relativo:
        return None
    bases = [
        Path(perfil.__file__).resolve().parent,  # pasta dash/
        Path.cwd() / "dash",
        Path.cwd(),
    ]
    for base in bases:
        caminho = (base / relativo).resolve()
        if caminho.is_file():
            return caminho
    return None


def render() -> None:
    dados = perfil.PERFIL

    coluna_texto, coluna_lado = st.columns([2.1, 1], gap="large")

    with coluna_texto:
        st.markdown(
            f"<div class='eyebrow' style='margin-top:0'>Perfil profissional</div>",
            unsafe_allow_html=True,
        )
        st.markdown(f"# {dados['nome']}")
        st.markdown(
            f"<p style='font-family:Space Grotesk,sans-serif;font-size:1.15rem;"
            f"color:{AMBAR};margin-top:-0.6rem'>{dados['cargo_alvo']}</p>"
            f"<p class='legenda' style='margin-top:-0.5rem'>{dados['subtitulo']}</p>",
            unsafe_allow_html=True,
        )

        for paragrafo in perfil.APRESENTACAO:
            st.markdown(f"<p class='legenda'>{paragrafo}</p>", unsafe_allow_html=True)

    with coluna_lado:
        foto_path = _arquivo_asset(dados.get("foto", ""))
        if foto_path is not None:
            st.image(foto_path.read_bytes(), use_container_width=True)

        linkedin = (dados.get("linkedin") or "").strip()
        github = (dados.get("github") or "").strip()
        contatos = [
            ("Local", dados["cidade"], None),
            ("E-mail", dados["email"],
             f"mailto:{dados['email']}" if dados.get("email") else None),
            ("Telefone", dados["telefone"], None),
            ("LinkedIn", "linkedin.com/in/arthur-canaverde", linkedin or None),
            ("GitHub", "github.com/CanaCruz", github or None),
        ]
        linhas = []
        for rotulo, valor, link in contatos:
            if not valor:
                continue
            if rotulo in ("LinkedIn", "GitHub", "E-mail") and not link:
                continue
            conteudo = (
                f"<a href='{link}' target='_blank' rel='noopener' "
                f"style='color:{AMBAR};text-decoration:none'>{valor}</a>"
                if link else valor
            )
            linhas.append(
                f"<div style='display:flex;justify-content:space-between;gap:1rem;"
                f"padding:0.45rem 0;border-bottom:1px solid #26303B;font-size:0.86rem'>"
                f"<span style='font-family:JetBrains Mono,monospace;font-size:0.7rem;"
                f"letter-spacing:0.1em;text-transform:uppercase;color:{SUAVE}'>{rotulo}</span>"
                f"<span style='text-align:right'>{conteudo}</span></div>"
            )
        st.markdown(
            "<div class='painel'><div class='meta'>Contato</div>"
            + "".join(linhas) + "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    ui.linha_kpis([
        {"rotulo": d["rotulo"], "valor": d["valor"], "nota": d["nota"],
         "destaque": i == 0}
        for i, d in enumerate(perfil.DESTAQUES)
    ])

    st.markdown(
        "<div class='eyebrow'>Sobre este dashboard</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='legenda'>Esta aplicação foi construída em Python com Streamlit e "
        "reúne, além da minha apresentação profissional, uma análise estatística "
        "aplicada sobre o mercado global de tecnologia, o setor em que pretendo "
        "atuar. O objetivo é demonstrar, no mesmo artefato, competência em "
        "desenvolvimento de aplicações e em análise de dados.</p>",
        unsafe_allow_html=True,
    )
