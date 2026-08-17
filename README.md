# Arthur Canaverde - Portfolio Dashboard

Portfólio profissional em Python/Streamlit: apresentação, qualificações, skills e uma análise estatística do mercado global de tecnologia, dados e IA.

**App online:** [arthur-canaverde-portfolio.streamlit.app](https://arthur-canaverde-portfolio-spy8bfkpp3eqwiqwkccp7q.streamlit.app/)

[LinkedIn](https://www.linkedin.com/in/arthur-canaverde-139a3a3a1/) | [GitHub](https://github.com/CanaCruz)

---

## O que tem no dashboard

| Aba | Conteúdo |
|---|---|
| **Quem sou eu** | Apresentação, contato e foco de carreira |
| **Minhas qualificações** | Formação, cursos/certificados, experiências e idiomas |
| **Skills** | Competências técnicas, soft skills, radar e projetos |
| **Análise de Dados** | Estudo salarial do mercado de tech (2020-2025) |

## Análise de dados

Base pública **Global Salaries in AI, ML & Data Science** ([ai-jobs.net](https://aijobs.net/salaries/), licença CC0), com cerca de 151 mil registros.

A análise cobre tratamento da base, estatística descritiva, segmentação (senioridade, regime, geografia, tempo), testes de hipótese, regressão log-linear e um simulador de percentil salarial.

## Stack

Python, Streamlit, Pandas, NumPy, SciPy, Plotly

## Rodar localmente

Requer Python 3.10+.

```bash
cd dash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Abre em `http://localhost:8501`.

## Estrutura

```
dash/
├── app.py                 # Entrada da aplicação
├── perfil.py              # Dados pessoais (único arquivo a personalizar)
├── requirements.txt
├── .streamlit/config.toml
├── assets/                # Foto e certificados
├── data/salaries.csv      # Base de análise
├── paginas/               # Abas do dashboard
└── src/                   # Dados, estatística, estilo e componentes
```

## Contato

- **E-mail:** canaverdearthur@gmail.com
- **LinkedIn:** [arthur-canaverde](https://www.linkedin.com/in/arthur-canaverde-139a3a3a1/)
- **GitHub:** [CanaCruz](https://github.com/CanaCruz)

---

Estudante de Engenharia de Software, FIAP 2ESA. Disponível para estágio após 11h40.
