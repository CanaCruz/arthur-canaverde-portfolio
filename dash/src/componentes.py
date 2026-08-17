"""
src/componentes.py
==================
Blocos de interface reutilizados pelas quatro abas do dashboard.
Cada função escreve HTML já estilizado por src/estilo.py.
"""

from typing import Iterable, Sequence

import streamlit as st


def cabecalho(titulo: str, subtitulo: str = "") -> None:
    """Título principal de uma aba."""
    st.markdown(f"# {titulo}")
    if subtitulo:
        st.markdown(f"<p class='legenda'>{subtitulo}</p>", unsafe_allow_html=True)


def secao(numero: str, titulo: str, descricao: str = "") -> None:
    """
    Cabeçalho de seção com marcador numerado.
    A numeração é usada apenas na aba de análise, onde as seções formam de fato
    uma sequência metodológica (base → descritiva → testes → modelo → conclusão).
    """
    st.markdown(f"<div class='eyebrow'>{numero}. {titulo}</div>",
                unsafe_allow_html=True)
    if descricao:
        st.markdown(f"<p class='legenda'>{descricao}</p>", unsafe_allow_html=True)


def kpi(rotulo: str, valor: str, nota: str = "", destaque: bool = False) -> None:
    """Cartão de indicador. Use dentro de um st.columns()."""
    classe = "kpi kpi-destaque" if destaque else "kpi"
    st.markdown(
        f"<div class='{classe}'>"
        f"<div class='kpi-rotulo'>{rotulo}</div>"
        f"<div class='kpi-valor'>{valor}</div>"
        f"<div class='kpi-nota'>{nota}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


def linha_kpis(itens: Sequence[dict]) -> None:
    """Renderiza uma faixa de cartões de indicador a partir de uma lista de dicts."""
    colunas = st.columns(len(itens))
    for coluna, item in zip(colunas, itens):
        with coluna:
            kpi(item["rotulo"], item["valor"], item.get("nota", ""),
                item.get("destaque", False))


def insight(texto: str) -> None:
    """Caixa de leitura do resultado. É aqui que a análise vira interpretação."""
    st.markdown(f"<div class='insight'>{texto}</div>", unsafe_allow_html=True)


def painel(titulo: str, meta: str = "", texto: str = "",
           itens: Iterable[str] = (), tags: Iterable[str] = ()) -> None:
    """Cartão de conteúdo usado em formação, experiência e projetos."""
    html = ["<div class='painel'>", f"<h4>{titulo}</h4>"]
    if meta:
        html.append(f"<div class='meta'>{meta}</div>")
    if texto:
        html.append(f"<p>{texto}</p>")
    itens = list(itens)
    if itens:
        html.append("<ul>" + "".join(f"<li>{i}</li>" for i in itens) + "</ul>")
    tags = list(tags)
    if tags:
        html.append("<div>" + "".join(f"<span class='tag'>{t}</span>" for t in tags)
                    + "</div>")
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def barra_nivel(nome: str, nivel: int) -> None:
    """Barra horizontal de proficiência (0 a 100)."""
    nivel = max(0, min(100, int(nivel)))
    st.markdown(
        f"<div class='skill-linha'>"
        f"<div class='skill-topo'><span>{nome}</span><span>{nivel}</span></div>"
        f"<div class='skill-trilho'><div class='skill-barra' "
        f"style='width:{nivel}%'></div></div>"
        f"</div>",
        unsafe_allow_html=True,
    )


def moeda(valor: float, simbolo: str = "US$") -> str:
    """Formata número no padrão brasileiro: US$ 146.100."""
    return f"{simbolo} {valor:,.0f}".replace(",", ".")


def numero(valor: float, casas: int = 0) -> str:
    """Formata número no padrão brasileiro: 151.445 ou 1,96."""
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "@").replace(".", ",").replace("@", ".")
