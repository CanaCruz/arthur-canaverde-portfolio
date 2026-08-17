# Dashboard Profissional com Análise de Dados

**CP1 — Data Science and Statistical Computing · FIAP**

Aplicação em Python/Streamlit que reúne um portfólio profissional e uma análise
estatística aplicada sobre o mercado global de tecnologia, dados e IA
(151.445 registros salariais, 2020–2025).

---

## 1. O que editar antes de entregar

Só existe **um** arquivo a personalizar: [`perfil.py`](perfil.py).

Abra, procure por `[EDITAR]` e substitua pelos seus dados reais — nome, contato,
formação, cursos, experiências, skills e projetos. As três primeiras abas são
geradas inteiramente a partir dele. Nenhum outro arquivo precisa ser tocado.

Para incluir foto: salve a imagem em `assets/foto.jpg` e ajuste a chave
`"foto"` em `PERFIL`.

---

## 2. Rodar na sua máquina

Requer Python 3.10 ou superior.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

A aplicação abre em `http://localhost:8501`.

---

## 3. Publicar (obrigatório para a entrega)

O enunciado exige o dashboard **hospedado e funcionando** no momento da correção.
O caminho mais rápido é o Streamlit Community Cloud, que é gratuito.

1. Crie um repositório **público** no GitHub e suba todo o conteúdo desta pasta,
   incluindo `data/salaries.csv` (8 MB — bem abaixo do limite de 100 MB).
2. Acesse <https://share.streamlit.io> e entre com a conta do GitHub.
3. Clique em **New app** e selecione o repositório, o branch `main` e o arquivo
   principal `app.py`.
4. Clique em **Deploy**. O primeiro build leva de 2 a 4 minutos.
5. Guarde a URL gerada — é ela que vai no formulário de entrega.

Se algo falhar no build, o log aparece na própria tela: quase sempre é uma
biblioteca faltando em `requirements.txt`.

---

## 4. Estrutura do projeto

```
.
├── app.py                  Ponto de entrada: configuração, tema e navegação
├── perfil.py               ★ Seus dados pessoais — o único arquivo a editar
├── requirements.txt        Dependências fixadas
├── .streamlit/config.toml  Tema da aplicação
├── data/
│   └── salaries.csv        Base de dados (fonte no item 5)
├── src/
│   ├── dados.py            Carregamento, limpeza e enriquecimento da base
│   ├── estatistica.py      Funções estatísticas (descritiva, testes, OLS)
│   ├── estilo.py           Paleta, tipografia, CSS e template Plotly
│   └── componentes.py      Blocos de interface reutilizáveis
└── paginas/
    ├── quem_sou_eu.py      Aba 1 — apresentação profissional
    ├── qualificacoes.py    Aba 2 — formação, cursos, experiência, idiomas
    ├── skills.py           Aba 3 — competências técnicas e soft skills
    └── analise.py          Aba 4 — análise de dados (peso 7,0)
```

---

## 5. Base de dados

**Global Salaries in AI, ML & Data Science** — ai-jobs.net, licença CC0
(domínio público). Disponível em <https://ai-jobs.net/salaries/>.

| | |
|---|---|
| Registros | 151.445 |
| Variáveis | 11 originais + 7 derivadas |
| Período | 2020 a 2025 |
| Cobertura | 70+ países |

Cada linha é a autodeclaração anual de um profissional, com o salário já
convertido para dólares pela taxa média do ano de referência.

---

## 6. Conteúdo estatístico da análise

| Seção | Técnicas aplicadas |
|---|---|
| 01 · Base e tratamento | Tipos de variável, valores ausentes, duplicatas, outliers por Tukey (1,5·IQR) |
| 02 · Descritiva | Média, mediana, moda, desvio, CV, quartis, IQR, assimetria, curtose, IC 95% pela distribuição t, teste de normalidade de D'Agostino-Pearson, histograma, boxplot e distribuição acumulada |
| 03 · Segmentação | Comparação por senioridade, regime, porte, família ocupacional, país e série temporal |
| 04 · Inferência | ANOVA de um fator, Kruskal-Wallis, eta², teste t de Welch, Mann-Whitney U, d de Cohen, qui-quadrado de independência e V de Cramér |
| 05 · Modelagem | Correlação de Pearson e Spearman, regressão linear múltipla log-linear com variáveis dummy, R² ajustado, erros-padrão, valores-p e diagnóstico de resíduos |
| 06 · Aplicação | Cálculo de percentil para posicionamento salarial, com limitações explicitadas |

Cada resultado numérico vem acompanhado da interpretação em linguagem de
negócio, e as limitações metodológicas estão declaradas na seção 06.

---

## 7. Tecnologias

Python · Streamlit · Pandas · NumPy · SciPy · Plotly
