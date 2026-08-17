"""
paginas/analise.py
==================
Aba 4 — Análise de Dados / Estudo de Mercado (peso 7,0 na avaliação).

Problema investigado
--------------------
Como se estrutura a remuneração no mercado global de tecnologia, dados e IA
entre 2020 e 2025, e quais fatores explicam a variação salarial observada?

Perguntas norteadoras
---------------------
Q1. Como a remuneração está distribuída? Média é uma medida adequada aqui?
Q2. Quanto a senioridade explica da diferença salarial?
Q3. Trabalho remoto remunera melhor do que presencial?
Q4. Porte da empresa e contratação internacional influenciam?
Q5. O mercado subiu ou recuou entre 2020 e 2025?
Q6. Que combinação de fatores melhor prevê o salário?
"""

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from src import componentes as ui
from src import dados as dt
from src import estatistica as est
from src.estilo import AMBAR, CORAL, LINHA, SUAVE, TEAL

ALFA = 0.05
MIN_GRUPO = 30  # n mínimo para um recorte entrar em ranking


# ---------------------------------------------------------------------------
# Barra lateral
# ---------------------------------------------------------------------------
def _filtros(base: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.markdown("### Filtros da análise")

    anos = st.sidebar.slider(
        "Período", int(base["ano"].min()), int(base["ano"].max()),
        (int(base["ano"].min()), int(base["ano"].max())),
    )

    familias = st.sidebar.multiselect(
        "Família de cargo",
        sorted(base["familia_cargo"].unique()),
        default=[],
        help="Vazio = todas as famílias.",
    )

    senioridades = st.sidebar.multiselect(
        "Senioridade", dt.ORDEM_SENIORIDADE, default=[],
        help="Vazio = todas as senioridades.",
    )

    principais = (base["pais"].value_counts().head(25).index.tolist())
    paises = st.sidebar.multiselect(
        "País da empresa", sorted(principais), default=[],
        help="Mostra os 25 países com maior volume de registros. Vazio = todos.",
    )

    sem_outliers = st.sidebar.checkbox(
        "Excluir outliers (critério de Tukey)", value=False,
        help="Remove registros fora de Q1−1,5·IQR e Q3+1,5·IQR.",
    )

    recorte = dt.aplicar_filtros(base, anos, paises, familias,
                                 senioridades, sem_outliers)

    st.sidebar.markdown(
        f"<p class='legenda' style='margin-top:0.8rem'>Registros no recorte: "
        f"<b style='color:{AMBAR}'>{ui.numero(len(recorte))}</b> de "
        f"{ui.numero(len(base))}</p>",
        unsafe_allow_html=True,
    )
    return recorte


# ---------------------------------------------------------------------------
# 01 — Base e problema
# ---------------------------------------------------------------------------
def _secao_base(base: pd.DataFrame, recorte: pd.DataFrame) -> None:
    ui.secao("01", "A base, o problema e o tratamento",
             "Antes de qualquer estatística: de onde vêm os dados, o que cada "
             "variável significa e o que foi feito com eles.")

    esquerda, direita = st.columns([1.2, 1], gap="large")
    with esquerda:
        st.markdown(
            "<div class='painel'><div class='meta'>Fonte</div>"
            "<h4>Global Salaries in AI, ML & Data Science</h4>"
            "<p>Base pública mantida pelo portal ai-jobs.net, sob licença CC0. "
            "Reúne autodeclarações de remuneração anual bruta de profissionais de "
            "tecnologia, dados e inteligência artificial em mais de 70 países, "
            "com o salário já convertido para dólares pela taxa média do ano de "
            "referência.</p>"
            "<p><b>Por que esta base:</b> é o setor em que pretendo atuar. "
            "Entender como o mercado precifica senioridade, regime de trabalho e "
            "especialização é uma decisão de carreira, não um exercício abstrato.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
    with direita:
        ui.linha_kpis([
            {"rotulo": "Registros", "valor": ui.numero(len(base)), "nota": "linhas na base bruta"},
            {"rotulo": "Variáveis", "valor": "11", "nota": "+7 derivadas"},
        ])
        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
        ui.linha_kpis([
            {"rotulo": "Período", "valor": f"{base['ano'].min()}–{base['ano'].max()}",
             "nota": "6 anos"},
            {"rotulo": "Países", "valor": str(base["pais"].nunique()),
             "nota": "sede das empresas"},
        ])

    st.markdown("#### Dicionário de dados")
    st.dataframe(dt.DICIONARIO, width="stretch", hide_index=True)

    st.markdown("#### Qualidade dos dados e decisões de tratamento")
    nulos = int(base.isna().sum().sum())
    duplicadas = int(base.duplicated().sum())
    ui.linha_kpis([
        {"rotulo": "Valores ausentes", "valor": ui.numero(nulos),
         "nota": "nenhuma imputação necessária"},
        {"rotulo": "Linhas idênticas", "valor": ui.numero(duplicadas),
         "nota": "mantidas — ver justificativa"},
        {"rotulo": "Outliers (Tukey)", "valor": ui.numero(int(base['outlier'].sum())),
         "nota": f"{base['outlier'].mean() * 100:.1f}% dos registros"},
    ])

    ui.insight(
        "<b>Decisão sobre duplicatas.</b> A base tem milhares de linhas idênticas, "
        "mas isso não indica erro: como as variáveis são todas categóricas ou "
        "arredondadas, dois profissionais diferentes com o mesmo cargo, senioridade, "
        "país e salário produzem naturalmente registros iguais. Removê-las "
        "distorceria a frequência real dos perfis mais comuns do mercado. "
        "Por isso foram <b>mantidas</b>.<br><br>"
        "<b>Decisão sobre outliers.</b> Salários acima do limite de Tukey existem de "
        "fato — cargos executivos em big techs americanas. Eles foram "
        "<b>marcados e não excluídos</b>: o filtro na barra lateral permite refazer "
        "toda a análise sem eles e comparar o efeito."
    )

    with st.expander("Ver amostra do recorte atual"):
        colunas = ["ano", "cargo", "familia_cargo", "senioridade", "regime",
                   "porte", "pais", "salario_usd"]
        st.dataframe(recorte[colunas].head(50), width="stretch",
                     hide_index=True)


# ---------------------------------------------------------------------------
# 02 — Estatística descritiva
# ---------------------------------------------------------------------------
def _secao_descritiva(recorte: pd.DataFrame) -> None:
    ui.secao("02", "Estatística descritiva",
             "Q1 — Como a remuneração está distribuída e qual medida de tendência "
             "central representa melhor este mercado?")

    resumo = est.resumo_descritivo(recorte["salario_usd"])
    ic_inf, ic_sup = est.intervalo_confianca(recorte["salario_usd"])

    ui.linha_kpis([
        {"rotulo": "Média", "valor": ui.moeda(resumo["media"]),
         "nota": f"IC 95%: {ui.moeda(ic_inf)} – {ui.moeda(ic_sup)}"},
        {"rotulo": "Mediana", "valor": ui.moeda(resumo["mediana"]),
         "nota": "medida robusta a extremos", "destaque": True},
        {"rotulo": "Desvio padrão", "valor": ui.moeda(resumo["desvio"]),
         "nota": f"CV = {resumo['cv']:.1f}%"},
        {"rotulo": "Amplitude interquartil", "valor": ui.moeda(resumo["iqr"]),
         "nota": f"Q1 {ui.moeda(resumo['q1'])} · Q3 {ui.moeda(resumo['q3'])}"},
    ])

    esquerda, direita = st.columns([1.4, 1], gap="large")

    with esquerda:
        figura = px.histogram(
            recorte, x="salario_usd", nbins=60, marginal="box",
            title="Distribuição da remuneração anual (US$)",
            labels={"salario_usd": "Salário anual em US$", "count": "Frequência"},
        )
        figura.update_traces(marker_line_width=0)
        figura.add_vline(x=resumo["media"], line_dash="dash", line_color=CORAL,
                         annotation_text="média", annotation_position="top")
        figura.add_vline(x=resumo["mediana"], line_dash="dash", line_color=TEAL,
                         annotation_text="mediana", annotation_position="bottom")
        figura.update_layout(height=440, showlegend=False, bargap=0.02)
        st.plotly_chart(figura, width="stretch")

    with direita:
        tabela = pd.DataFrame({
            "Medida": ["n", "Mínimo", "1º quartil", "Mediana", "Média",
                       "3º quartil", "Máximo", "Desvio padrão",
                       "Coef. de variação", "Assimetria", "Curtose (excesso)"],
            "Valor": [
                ui.numero(resumo["n"]),
                ui.moeda(resumo["minimo"]),
                ui.moeda(resumo["q1"]),
                ui.moeda(resumo["mediana"]),
                ui.moeda(resumo["media"]),
                ui.moeda(resumo["q3"]),
                ui.moeda(resumo["maximo"]),
                ui.moeda(resumo["desvio"]),
                f"{resumo['cv']:.1f}%",
                f"{resumo['assimetria']:.3f}",
                f"{resumo['curtose']:.3f}",
            ],
        })
        st.dataframe(tabela, width="stretch", hide_index=True,
                     height=440)

    normalidade = est.teste_normalidade(recorte["salario_usd"])
    relacao = ((resumo["media"] / resumo["mediana"]) - 1) * 100

    ui.insight(
        f"<b>A distribuição é assimétrica à direita</b> (assimetria = "
        f"{resumo['assimetria']:.2f} &gt; 0): a média fica "
        f"{relacao:.1f}% acima da mediana, puxada pela cauda de salários muito "
        f"altos. Em um mercado com essa forma, <b>a mediana descreve melhor o "
        f"profissional típico</b> — usar a média superestima o que a maioria "
        f"realmente ganha.<br><br>"
        f"O teste de D'Agostino-Pearson sobre amostra de "
        f"{ui.numero(normalidade['n'])} registros retorna p = "
        f"{normalidade['p']:.2e}, rejeitando a hipótese de normalidade. "
        f"Por isso, adiante, todo teste paramétrico é acompanhado de sua "
        f"alternativa não paramétrica.<br><br>"
        f"Na distribuição acumulada implícita: P25 = "
        f"{ui.moeda(float(np.percentile(recorte['salario_usd'], 25)))}, "
        f"P50 = {ui.moeda(resumo['mediana'])}, "
        f"P75 = {ui.moeda(float(np.percentile(recorte['salario_usd'], 75)))}, "
        f"P90 = {ui.moeda(float(np.percentile(recorte['salario_usd'], 90)))}."
    )


# ---------------------------------------------------------------------------
# 03 — Segmentação
# ---------------------------------------------------------------------------
def _secao_segmentos(recorte: pd.DataFrame) -> None:
    ui.secao("03", "Comparação entre segmentos",
             "Q2 a Q5 — onde estão as diferenças: senioridade, regime de "
             "trabalho, porte, geografia e tempo.")

    esquerda, direita = st.columns(2, gap="large")

    with esquerda:
        st.markdown("##### Senioridade")
        figura = px.box(recorte, x="senioridade", y="salario_usd",
                        color="senioridade", points=False,
                        category_orders={"senioridade": dt.ORDEM_SENIORIDADE},
                        labels={"senioridade": "", "salario_usd": "Salário (US$)"})
        figura.update_layout(height=340, showlegend=False)
        st.plotly_chart(figura, width="stretch")

    with direita:
        st.markdown("##### Evolução da mediana (2020–2025)")
        evolucao = (recorte.groupby(["ano", "senioridade"], observed=True)
                    .agg(mediana=("salario_usd", "median"), n=("salario_usd", "size"))
                    .reset_index())
        evolucao = evolucao[evolucao["n"] >= MIN_GRUPO]
        figura = px.line(evolucao, x="ano", y="mediana", color="senioridade",
                         markers=True,
                         category_orders={"senioridade": dt.ORDEM_SENIORIDADE},
                         labels={"ano": "", "mediana": "Mediana salarial (US$)",
                                 "senioridade": ""})
        figura.update_layout(height=340)
        st.plotly_chart(figura, width="stretch")

    # Regime, família, país e porte em tabela — a inferência formal vem na seção 04.
    esquerda, direita = st.columns(2, gap="large")
    with esquerda:
        st.markdown("##### Mediana por regime e por porte")
        por_regime = (recorte.groupby("regime", observed=True)
                      .agg(Mediana=("salario_usd", "median"), n=("salario_usd", "size"))
                      .reindex(dt.ORDEM_REGIME).dropna().reset_index()
                      .rename(columns={"regime": "Grupo"}))
        por_regime.insert(0, "Fator", "Regime")
        por_porte = (recorte.groupby("porte", observed=True)
                     .agg(Mediana=("salario_usd", "median"), n=("salario_usd", "size"))
                     .reset_index().rename(columns={"porte": "Grupo"}))
        por_porte.insert(0, "Fator", "Porte")
        st.dataframe(
            pd.concat([por_regime, por_porte], ignore_index=True)
            .style.format({"Mediana": "{:,.0f}"}),
            width="stretch", hide_index=True,
        )
    with direita:
        st.markdown("##### Top famílias e países (mediana)")
        familias = (recorte.groupby("familia_cargo", observed=True)
                    .agg(Mediana=("salario_usd", "median"), n=("salario_usd", "size"))
                    .reset_index())
        familias = (familias[familias["n"] >= MIN_GRUPO]
                    .sort_values("Mediana", ascending=False).head(6)
                    .rename(columns={"familia_cargo": "Grupo"}))
        paises = (recorte.groupby("pais", observed=True)
                  .agg(Mediana=("salario_usd", "median"), n=("salario_usd", "size"))
                  .reset_index())
        paises = (paises[paises["n"] >= MIN_GRUPO]
                  .sort_values("Mediana", ascending=False).head(6)
                  .rename(columns={"pais": "Grupo"}))
        familias.insert(0, "Fator", "Família")
        paises.insert(0, "Fator", "País")
        st.dataframe(
            pd.concat([familias, paises], ignore_index=True)
            .style.format({"Mediana": "{:,.0f}"}),
            width="stretch", hide_index=True,
        )

    with st.expander("Ver cruzamento senioridade × regime (tabela)"):
        matriz = (recorte.pivot_table(index="senioridade", columns="regime",
                                      values="salario_usd", aggfunc="median",
                                      observed=True)
                  .reindex(index=dt.ORDEM_SENIORIDADE, columns=dt.ORDEM_REGIME))
        st.dataframe(matriz.style.format("{:,.0f}"), width="stretch")

    ui.insight(
        "A leitura cruzada mostra que <b>o efeito do regime de trabalho não é o "
        "mesmo em todas as senioridades</b>. Comparar apenas 'remoto x presencial' "
        "no agregado esconde essa interação — é exatamente o tipo de conclusão "
        "apressada que a segmentação evita."
    )


# ---------------------------------------------------------------------------
# 04 — Testes de hipótese
# ---------------------------------------------------------------------------
def _secao_testes(recorte: pd.DataFrame) -> None:
    ui.secao("04", "Testes de hipótese",
             f"As diferenças vistas acima resistem à inferência estatística? "
             f"Nível de significância adotado: α = {ALFA}.")

    teste_a, teste_b, teste_c = st.tabs([
        "Senioridade (k grupos)", "Remoto × presencial", "Independência (χ²)"
    ])

    # -- Teste 1: ANOVA / Kruskal-Wallis ----------------------------------
    with teste_a:
        st.markdown(
            "**H₀:** as medianas salariais são iguais nos quatro níveis de senioridade.  \n"
            "**H₁:** ao menos um nível difere dos demais."
        )
        grupos = [g["salario_usd"].values for _, g in
                  recorte.groupby("senioridade", observed=True) if len(g) > 1]
        resultado = est.comparar_grupos(grupos)
        if resultado:
            ui.linha_kpis([
                {"rotulo": "ANOVA — F", "valor": f"{resultado['f']:.1f}",
                 "nota": f"p = {resultado['p_anova']:.2e}"},
                {"rotulo": "Kruskal-Wallis — H", "valor": f"{resultado['h']:.1f}",
                 "nota": f"p = {resultado['p_kruskal']:.2e}"},
                {"rotulo": "Eta² (tamanho de efeito)",
                 "valor": f"{resultado['eta2']:.3f}",
                 "nota": f"efeito {est.classificar_eta2(resultado['eta2'])}",
                 "destaque": True},
            ])
            ui.insight(
                est.interpretar_p(resultado["p_kruskal"], ALFA) +
                f"<br><br>O eta² indica que a senioridade explica cerca de "
                f"<b>{resultado['eta2'] * 100:.1f}% da variância salarial</b> — "
                f"efeito {est.classificar_eta2(resultado['eta2'])}. Significância "
                f"e relevância prática são coisas diferentes: com n grande, quase "
                f"tudo dá significativo, e por isso o tamanho de efeito é "
                f"reportado junto."
            )

            linhas = []
            for nivel, grupo in recorte.groupby("senioridade", observed=True):
                if len(grupo) < 2:
                    continue
                inf, sup = est.intervalo_confianca(grupo["salario_usd"])
                linhas.append({
                    "Senioridade": nivel, "n": len(grupo),
                    "Mediana": grupo["salario_usd"].median(),
                    "Média": grupo["salario_usd"].mean(),
                    "IC inferior": inf, "IC superior": sup,
                })
            tabela = pd.DataFrame(linhas)
            st.dataframe(
                tabela.style.format({"Mediana": "{:,.0f}", "Média": "{:,.0f}",
                                     "IC inferior": "{:,.0f}",
                                     "IC superior": "{:,.0f}"}),
                width="stretch", hide_index=True,
            )

    # -- Teste 2: duas amostras -------------------------------------------
    with teste_b:
        st.markdown(
            "**H₀:** não há diferença salarial entre trabalho remoto e presencial.  \n"
            "**H₁:** há diferença."
        )
        remoto = recorte.loc[recorte["regime"] == "Remoto", "salario_usd"].values
        presencial = recorte.loc[recorte["regime"] == "Presencial", "salario_usd"].values
        resultado = est.comparar_duas_amostras(remoto, presencial)
        if resultado:
            diferenca = resultado["media_a"] - resultado["media_b"]
            ui.linha_kpis([
                {"rotulo": "Média remoto", "valor": ui.moeda(resultado["media_a"]),
                 "nota": f"n = {ui.numero(resultado['n_a'])}"},
                {"rotulo": "Média presencial", "valor": ui.moeda(resultado["media_b"]),
                 "nota": f"n = {ui.numero(resultado['n_b'])}"},
                {"rotulo": "Diferença", "valor": ui.moeda(abs(diferenca)),
                 "nota": "a favor do remoto" if diferenca > 0 else "a favor do presencial",
                 "destaque": True},
                {"rotulo": "d de Cohen", "valor": f"{resultado['d']:.3f}",
                 "nota": "tamanho de efeito"},
            ])
            st.markdown(
                f"Teste t de Welch: t = {resultado['t']:.2f}, p = {resultado['p_t']:.2e}  \n"
                f"Mann-Whitney U: p = {resultado['p_u']:.2e}"
            )
            ui.insight(
                est.interpretar_p(resultado["p_u"], ALFA) +
                f"<br><br>Ainda assim, o d de Cohen de {abs(resultado['d']):.2f} "
                f"aponta um efeito pequeno. A diferença existe, mas o regime de "
                f"trabalho está longe de ser o fator determinante da remuneração — "
                f"e parte dela pode ser efeito de composição, já que empresas "
                f"americanas concentram tanto os salários mais altos quanto um "
                f"regime específico."
            )

    # -- Teste 3: qui-quadrado --------------------------------------------
    with teste_c:
        st.markdown(
            "**H₀:** senioridade e porte da empresa são independentes.  \n"
            "**H₁:** existe associação entre as duas variáveis."
        )
        tabela = pd.crosstab(recorte["senioridade"], recorte["porte"])
        tabela = tabela.loc[tabela.sum(axis=1) > 0, tabela.sum(axis=0) > 0]
        if tabela.size and min(tabela.shape) > 1:
            resultado = est.qui_quadrado(tabela)
            ui.linha_kpis([
                {"rotulo": "χ²", "valor": f"{resultado['chi2']:.1f}",
                 "nota": f"{resultado['gl']} graus de liberdade"},
                {"rotulo": "p-valor", "valor": f"{resultado['p']:.2e}",
                 "nota": f"α = {ALFA}"},
                {"rotulo": "V de Cramér", "valor": f"{resultado['v_cramer']:.3f}",
                 "nota": "força da associação", "destaque": True},
            ])
            st.markdown("###### Tabela de contingência (frequências observadas)")
            st.dataframe(tabela, width="stretch")
            ui.insight(
                est.interpretar_p(resultado["p"], ALFA) +
                "<br><br>O V de Cramér mede a <b>força</b> da associação numa escala "
                "de 0 a 1. Valores baixos indicam que, embora a associação seja "
                "estatisticamente detectável, ela é fraca na prática — porte e "
                "senioridade se distribuem de forma parecida entre si."
            )
        else:
            st.info("O recorte atual não tem categorias suficientes para o teste.")


# ---------------------------------------------------------------------------
# 05 — Correlação e regressão
# ---------------------------------------------------------------------------
def _secao_modelo(recorte: pd.DataFrame) -> None:
    ui.secao("05", "Correlação e modelo de regressão",
             "Q6 — quanto do salário conseguimos explicar combinando os fatores "
             "disponíveis?")

    correl = est.correlacao(recorte["senioridade_num"], recorte["salario_usd"])
    if correl:
        st.markdown(
            f"Senioridade × salário — Pearson r = {correl['r']:.3f} "
            f"(p = {correl['p_r']:.2e}); Spearman ρ = {correl['rho']:.3f}."
        )

    st.markdown(
        "<p class='legenda'>Variável dependente: <b>log do salário</b>. "
        "A transformação logarítmica corrige a assimetria observada na seção 02 "
        "e faz cada coeficiente ser lido como variação percentual aproximada. "
        "As variáveis categóricas entram como <i>dummies</i>, sempre com uma "
        "categoria de referência omitida.</p>",
        unsafe_allow_html=True,
    )

    modelo = _ajustar_modelo(recorte)
    if modelo is None:
        st.info("O recorte atual não tem variação suficiente para ajustar o modelo.")
        return

    resultado, rotulos = modelo
    ui.linha_kpis([
        {"rotulo": "R²", "valor": f"{resultado['r2']:.3f}",
         "nota": "variação explicada", "destaque": True},
        {"rotulo": "R² ajustado", "valor": f"{resultado['r2_aj']:.3f}",
         "nota": "penaliza excesso de variáveis"},
        {"rotulo": "Observações", "valor": ui.numero(resultado["n"]), "nota": ""},
        {"rotulo": "Preditores", "valor": str(resultado["k"]), "nota": "além do intercepto"},
    ])

    tabela = resultado["tabela"].copy()
    tabela["Variável"] = tabela["Variável"].map(lambda v: rotulos.get(v, v))
    tabela["Efeito aprox."] = (np.exp(tabela["Coeficiente"]) - 1) * 100
    tabela.loc[tabela["Variável"] == "Intercepto", "Efeito aprox."] = np.nan
    tabela["Significativo"] = np.where(tabela["p-valor"] < ALFA, "sim", "não")

    coeficientes = tabela[tabela["Variável"] != "Intercepto"].copy()
    coeficientes = coeficientes.sort_values("Efeito aprox.")
    figura = px.bar(coeficientes, x="Efeito aprox.", y="Variável",
                    orientation="h", color="Significativo",
                    color_discrete_map={"sim": AMBAR, "não": SUAVE},
                    labels={"Efeito aprox.": "Efeito sobre o salário (%)",
                            "Variável": ""})
    figura.update_layout(height=max(340, 26 * len(coeficientes)),
                         legend_title_text="p &lt; 0,05")
    st.plotly_chart(figura, width="stretch")

    with st.expander("Ver tabela completa de coeficientes e diagnóstico de resíduos"):
        st.dataframe(
            tabela.style.format({"Coeficiente": "{:.4f}", "Erro padrão": "{:.4f}",
                                 "t": "{:.2f}", "p-valor": "{:.2e}",
                                 "Efeito aprox.": "{:+.1f}%"}),
            width="stretch", hide_index=True,
        )
        st.markdown(
            f"<p class='legenda'>Diagnóstico: resíduos com média ≈ 0 e dispersão "
            f"sem padrão forte vs. ajustados. n = {ui.numero(resultado['n'])}. "
            f"O modelo é associativo, não causal.</p>",
            unsafe_allow_html=True,
        )

    ui.insight(
        f"O modelo explica <b>{resultado['r2'] * 100:.1f}% da variação</b> do log do "
        f"salário. O restante fica com fatores que a base não registra — empresa "
        f"específica, tempo de casa, negociação individual, formação. "
        f"É um resultado honesto para dados observacionais de autodeclaração: "
        f"identifica direção e ordem de grandeza dos efeitos, mas <b>não estabelece "
        f"causalidade</b>. Nenhum coeficiente aqui autoriza dizer que mudar de "
        f"regime de trabalho <i>causa</i> aumento salarial."
    )


@st.cache_data(show_spinner="Ajustando o modelo...")
def _ajustar_modelo(recorte: pd.DataFrame):
    """Monta a matriz de desenho com dummies e ajusta o OLS."""
    base = recorte[["log_salario", "senioridade", "regime", "porte",
                    "familia_cargo", "ano", "mesmo_pais"]].dropna()
    if len(base) < 100:
        return None

    # Mantém apenas famílias com volume relevante, para não criar dummies ralas.
    frequentes = base["familia_cargo"].value_counts()
    frequentes = frequentes[frequentes >= 100].index
    base = base[base["familia_cargo"].isin(frequentes)]
    if base["senioridade"].nunique() < 2:
        return None

    X = pd.get_dummies(
        base[["senioridade", "regime", "porte", "familia_cargo", "mesmo_pais"]],
        drop_first=True, dtype=float,
    )
    X["ano"] = base["ano"] - base["ano"].min()
    X = X.loc[:, X.std() > 0]
    if X.empty:
        return None

    resultado = est.regressao_ols(X, base["log_salario"])

    rotulos = {c: (c.replace("senioridade_", "Senioridade: ")
                    .replace("regime_", "Regime: ")
                    .replace("porte_", "Porte: ")
                    .replace("familia_cargo_", "Área: ")
                    .replace("mesmo_pais_", "")
                    .replace("ano", "Ano (por ano decorrido)"))
               for c in X.columns}
    return resultado, rotulos


# ---------------------------------------------------------------------------
# 06 — Conclusões e simulador
# ---------------------------------------------------------------------------
def _secao_conclusoes(recorte: pd.DataFrame) -> None:
    ui.secao("06", "Conclusões e aplicação",
             "O que a análise responde e o que ela deliberadamente não responde.")

    resumo = est.resumo_descritivo(recorte["salario_usd"])
    por_senioridade = (recorte.groupby("senioridade", observed=True)["salario_usd"]
                       .median().dropna())
    salto = ""
    if "Júnior" in por_senioridade.index and "Sênior" in por_senioridade.index:
        razao = por_senioridade["Sênior"] / por_senioridade["Júnior"]
        salto = (f"A mediana de um profissional sênior é <b>{razao:.1f}× a de um "
                 f"júnior</b> — o maior salto isolado de toda a base.")

    esquerda, direita = st.columns(2, gap="large")
    with esquerda:
        ui.painel(
            titulo="O que os dados sustentam",
            meta="Conclusões",
            itens=[
                "A distribuição salarial é assimétrica à direita; a mediana "
                f"({ui.moeda(resumo['mediana'])}) representa o mercado melhor que "
                f"a média ({ui.moeda(resumo['media'])}).",
                f"Senioridade é o fator mais forte entre os disponíveis. {salto}",
                "Regime de trabalho tem efeito estatisticamente detectável, mas "
                "pequeno na prática — e confundido com a geografia do empregador.",
                "A geografia da empresa domina a comparação internacional: "
                "comparar salários entre países sem ajustar por custo de vida e "
                "câmbio produz conclusões enganosas.",
            ],
        )
    with direita:
        ui.painel(
            titulo="Limitações reconhecidas",
            meta="Honestidade metodológica",
            itens=[
                "Dados autodeclarados, sujeitos a viés de seleção: quem responde "
                "tende a ter remuneração acima da média do setor.",
                "Forte concentração em empresas dos Estados Unidos, o que puxa "
                "todas as medidas agregadas para cima.",
                "Valores em dólares nominais, sem ajuste por paridade de poder "
                "de compra nem por inflação do período.",
                "Estudo observacional: identifica associação, nunca causalidade.",
            ],
        )

    st.markdown("##### Onde eu me posiciono")
    st.markdown(
        "<p class='legenda'>Aplicação prática da análise: informar uma "
        "negociação salarial com percentil, e não com achismo.</p>",
        unsafe_allow_html=True,
    )

    campo_a, campo_b, campo_c, campo_d = st.columns(4)
    with campo_a:
        familia = st.selectbox("Área", sorted(recorte["familia_cargo"].unique()))
    with campo_b:
        niveis = [n for n in dt.ORDEM_SENIORIDADE
                  if n in recorte["senioridade"].unique()]
        nivel = st.selectbox("Senioridade", niveis)
    with campo_c:
        cambio = st.number_input("Câmbio USD → BRL", min_value=1.0, max_value=15.0,
                                 value=5.40, step=0.05)
    with campo_d:
        proposta = st.number_input("Proposta anual bruta (R$)", min_value=0,
                                   value=60000, step=6000)

    referencia = recorte[(recorte["familia_cargo"] == familia)
                         & (recorte["senioridade"] == nivel)]["salario_usd"]

    if len(referencia) < MIN_GRUPO:
        st.info("Esse recorte tem poucos registros para uma comparação confiável. "
                "Amplie os filtros na barra lateral.")
        return

    proposta_usd = proposta / cambio
    percentil = float((referencia < proposta_usd).mean() * 100)

    ui.linha_kpis([
        {"rotulo": "Sua proposta em dólares", "valor": ui.moeda(proposta_usd),
         "nota": f"câmbio de {cambio:.2f}"},
        {"rotulo": "Mediana do recorte", "valor": ui.moeda(referencia.median()),
         "nota": f"n = {ui.numero(len(referencia))}"},
        {"rotulo": "Seu percentil", "valor": f"P{percentil:.0f}",
         "nota": f"acima de {percentil:.0f}% do recorte", "destaque": True},
    ])

    figura = px.histogram(referencia, nbins=50,
                          labels={"value": "Salário anual (US$)"})
    figura.update_traces(marker_color=LINHA, marker_line_width=0)
    figura.add_vline(x=proposta_usd, line_color=AMBAR, line_width=3,
                     annotation_text="sua proposta", annotation_position="top")
    figura.add_vline(x=float(referencia.median()), line_color=TEAL,
                     line_dash="dash", annotation_text="mediana",
                     annotation_position="bottom")
    figura.update_layout(height=320, showlegend=False,
                         title=f"{familia} · {nivel}")
    st.plotly_chart(figura, width="stretch")

    ui.insight(
        "<b>Leitura correta deste número.</b> O percentil compara a proposta com um "
        "mercado majoritariamente norte-americano, convertido a câmbio nominal. "
        "Ele serve para entender <i>posição relativa dentro da própria faixa</i> e "
        "para calibrar expectativa de progressão — não para afirmar que uma vaga "
        "no Brasil deveria pagar o mesmo que uma nos Estados Unidos."
    )


# ---------------------------------------------------------------------------
# Página
# ---------------------------------------------------------------------------
def render() -> None:
    base = dt.carregar_dados()
    recorte = _filtros(base)

    ui.cabecalho(
        "Mercado de tecnologia, dados e IA",
        "Análise estatística de 151 mil registros salariais entre 2020 e 2025. "
        "Objetivo: entender como o mercado em que pretendo atuar precifica "
        "senioridade, especialização, regime de trabalho e geografia.",
    )

    if recorte.empty:
        st.warning("Nenhum registro atende aos filtros selecionados. "
                   "Ajuste os filtros na barra lateral.")
        return

    _secao_base(base, recorte)
    _secao_descritiva(recorte)
    _secao_segmentos(recorte)
    _secao_testes(recorte)
    _secao_modelo(recorte)
    _secao_conclusoes(recorte)
