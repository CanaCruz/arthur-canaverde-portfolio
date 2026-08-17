"""
perfil.py
=========
ÚNICO arquivo que você precisa editar para personalizar o dashboard.
Todo o conteúdo das abas "Quem sou eu", "Minhas qualificações" e "Skills"
vem daqui. Nenhuma alteração é necessária nos demais arquivos.

>>> Personalize em PERFIL. A foto e os certificados usam caminhos relativos à pasta do app. <<<
"""

# ---------------------------------------------------------------------------
# 1. IDENTIFICAÇÃO
# ---------------------------------------------------------------------------
PERFIL = {
    "nome": "Arthur Canaverde da Cruz",
    "cargo_alvo": "Estudante de Engenharia de Software · FIAP 2ESA",
    "subtitulo": "Desenvolvimento full stack · Dados · Automação",
    "cidade": "São Paulo, SP — Brasil",
    "email": "canaverdearthur@gmail.com",
    "telefone": "(11) 94761-9435",
    "linkedin": "https://www.linkedin.com/in/arthur-canaverde-139a3a3a1/",
    "github": "https://github.com/CanaCruz",
    "foto": "assets/foto.jpg",
}

# Texto de apresentação. Cada item da lista vira um parágrafo.
APRESENTACAO = [
    "Sou estudante de Engenharia de Software na FIAP (turma 2ESA), com previsão "
    "de formatura em dezembro de 2028. Venho do Colégio São Francisco Xavier "
    "(Sanfra) e, desde que entrei na graduação, tenho concentrado a prática em "
    "desenvolvimento web, análise de dados e projetos aplicados — tanto "
    "acadêmicos quanto challenges com empresa.",

    "No dia a dia, gosto de fechar o ciclo: entender o problema, modelar a "
    "informação, construir a interface e validar o resultado. Já trabalhei com "
    "React, TypeScript e Tailwind em dashboards de produto, com Python e "
    "Streamlit em análise estatística, e com Arduino em solução IoT de "
    "monitoramento. O que me move é juntar código limpo com decisão baseada em "
    "dado, e não em achismo.",

    "No Challenge FIAP × TOTVS, por exemplo, construí um dashboard para analisar "
    "mais de mil transcrições de reuniões comerciais — com foco em desempenho, "
    "organização da base e publicação automatizada. Em paralelo, este próprio "
    "dashboard reúne meu portfólio com uma análise do mercado global de "
    "tecnologia sobre 151 mil registros salariais.",

    "Busco um estágio em tecnologia para contribuir com desenvolvimento "
    "full stack e, ao mesmo tempo, aprofundar atuação em engenharia e análise "
    "de dados. Tenho disponibilidade em qualquer horário após o término das "
    "aulas (faculdade das 8h às 11h40).",
]

# Três frases curtas que aparecem como destaque no topo da página inicial.
DESTAQUES = [
    {"rotulo": "Formação", "valor": "Eng. de Software", "nota": "FIAP · 2ESA · 2025–2028"},
    {"rotulo": "Foco", "valor": "Full stack + Dados", "nota": "React · TypeScript · Python"},
    {"rotulo": "Objetivo", "valor": "Estágio 2026", "nota": "Disponível após 11h40"},
]

# ---------------------------------------------------------------------------
# 2. QUALIFICAÇÕES
# ---------------------------------------------------------------------------
FORMACAO = [
    {
        "curso": "Engenharia de Software — Bacharelado",
        "instituicao": "FIAP",
        "periodo": "2025 — dez/2028 (previsto)",
        "detalhe": "Turma 2ESA. Ênfase em desenvolvimento de software, arquitetura "
                   "de sistemas, banco de dados e ciência de dados.",
    },
    {
        "curso": "Ensino Médio",
        "instituicao": "Colégio São Francisco Xavier — Rede Jesuíta de Educação",
        "periodo": "2022 — 2024",
        "detalhe": "Ipiranga, São Paulo (Sanfra).",
    },
]

CURSOS = [
    {
        "nome": "Design Thinking – Process (40h)",
        "emissor": "FIAP Nano Course",
        "ano": "04/mai/2025",
        "arquivo": "assets/certificados/Design-Thinking-Process.pdf",
    },
    {
        "nome": "Formação Social e Sustentabilidade (80h)",
        "emissor": "FIAP Nano Course",
        "ano": "02/mai/2025",
        "arquivo": "assets/certificados/Formacao-Social-e-Sustentabilidade.pdf",
    },
]

EXPERIENCIAS = [
    {
        "cargo": "Desenvolvedor front-end — TOTVS Insight",
        "empresa": "Challenge FIAP × TOTVS",
        "periodo": "2026 — atual",
        "atividades": [
            "Participei do Challenge da FIAP com a TOTVS, construindo um dashboard "
            "de análise de 1.126 transcrições de reuniões comerciais em React 19, "
            "TypeScript, Vite e Tailwind CSS.",
            "Projetei a camada de dados para quebrar um dump NDJSON de 46 MB em um "
            "índice de 470 KB mais um arquivo por transcrição, derrubando o "
            "carregamento inicial para menos de 1 MB.",
            "Separei a leitura dos dados em um único módulo: as telas não buscam "
            "arquivo nem conhecem o formato da origem — só pedem o que precisam. "
            "Assim, trocar o dump estático por uma API depois fica mais simples. "
            "Também configurei publicação automática no GitHub Pages a cada push.",
        ],
    },
    {
        "cargo": "Desenvolvedor — Sistema de alerta de enchentes",
        "empresa": "Global Solution · FIAP",
        "periodo": "2025",
        "atividades": [
            "Construí em Arduino Uno e C++ um monitor de nível de água com sensor "
            "ultrassônico HC-SR04, LCD 16x2, LEDs de risco e alerta sonoro.",
            "Implementei a lógica de faixas de risco por percentual de enchimento, "
            "acionando buzzer acima de 90% da profundidade configurada.",
        ],
    },
]

IDIOMAS = [
    {"idioma": "Português", "nivel": "Nativo", "escala": 100},
    {"idioma": "Inglês", "nivel": "Intermediário", "escala": 60},
    {"idioma": "Espanhol", "nivel": "Básico", "escala": 35},
]

# ---------------------------------------------------------------------------
# 3. SKILLS
# ---------------------------------------------------------------------------
# nivel: 0 a 100. Seja honesto — recrutador costuma perguntar.
SKILLS_TECNICAS = {
    "Linguagens": [
        {"nome": "JavaScript", "nivel": 70},
        {"nome": "TypeScript", "nivel": 75},
        {"nome": "Python", "nivel": 75},
        {"nome": "HTML / CSS", "nivel": 85},
        {"nome": "SQL", "nivel": 60},
        {"nome": "C++ (Arduino)", "nivel": 45},
    ],
    "Frameworks e bibliotecas": [
        {"nome": "React", "nivel": 75},
        {"nome": "Tailwind CSS", "nivel": 70},
        {"nome": "Node.js", "nivel": 60},
        {"nome": "Pandas", "nivel": 60},
        {"nome": "Streamlit", "nivel": 55},
    ],
    "Ferramentas e plataformas": [
        {"nome": "Git / GitHub", "nivel": 75},
        {"nome": "Vite", "nivel": 65},
        {"nome": "VS Code", "nivel": 85},
        {"nome": "Docker", "nivel": 25},
    ],
}

SOFT_SKILLS = [
    {"nome": "Comunicação", "descricao": "Traduzo problema técnico para linguagem de negócio."},
    {"nome": "Trabalho em equipe", "descricao": "Experiência com metodologias ágeis e code review."},
    {"nome": "Autonomia de estudo", "descricao": "Aprendo stack nova por documentação oficial."},
    {"nome": "Pensamento analítico", "descricao": "Quebro o problema antes de escrever a primeira linha."},
    {"nome": "Organização", "descricao": "Uso Kanban e versionamento em todo projeto."},
]

# Aparece no radar da aba Skills — máximo 6 eixos fica legível.
RADAR = {
    "Front-end": 80,
    "Back-end": 60,
    "Banco de dados": 60,
    "Análise de dados": 60,
    "Estatística": 55,
    "Versionamento": 75,
}

PROJETOS = [
    {
        "titulo": "TOTVS Insight",
        "descricao": "Challenge FIAP × TOTVS: dashboard de análise de 1.126 "
                     "transcrições de reuniões comerciais — indicadores, "
                     "distribuições e histórico por cliente, com carga sob "
                     "demanda de uma base de 46 MB.",
        "stack": ["React 19", "TypeScript", "Vite", "Tailwind CSS"],
        "link": "https://github.com/CanaCruz/TOTVS-Insigth",
    },
    {
        "titulo": "Alerta de Enchentes com Arduino",
        "descricao": "Monitor de nível de água com sensor ultrassônico, LCD e "
                     "alerta visual e sonoro por faixa de risco, para bairros sem "
                     "monitoramento adequado.",
        "stack": ["C++", "Arduino Uno", "HC-SR04"],
        "link": "https://github.com/CanaCruz/GS-Arduino",
    },
    {
        "titulo": "Dashboard de Análise do Mercado de Tecnologia",
        "descricao": "Aplicação em Streamlit com análise estatística de 151 mil "
                     "registros salariais do mercado global de tecnologia "
                     "(CP1 · turma 2ESA · entrega 24/08).",
        "stack": ["Python", "Pandas", "Plotly", "SciPy", "Streamlit"],
        "link": "",
    },
]
