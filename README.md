# CRM Inteligente para Gestao de Marketing Digital

Projeto academico completo de CRM para organizar, qualificar e acompanhar leads de multiplos canais. O foco principal e CRM; a IA entra apenas como suporte para resumo de leads e geracao de follow-up.

## Objetivo

- Cadastro de leads e clientes
- Gestao de interacoes
- Pipeline de vendas em Kanban
- Lead Scoring baseado em regras
- Dashboard e relatorios
- Resumo inteligente de leads (IA)
- Geracao de follow-up (IA)

## Arquitetura em camadas

- Presentation Layer: templates e rotas
- Business Layer: services
- Data Layer: models e repositories
- AI Layer: agents e OllamaService

## Tecnologias

- Python 3.12+
- Flask, Flask-Login, Flask-Migrate, Flask-WTF, SQLAlchemy
- PostgreSQL
- Bootstrap 5, Chart.js
- Ollama com modelo local Qwen3 8B

## Estrutura de pastas

```
crm_ai/
  app/
    agents/
    models/
    repositories/
    routes/
    services/
    static/
    templates/
    __init__.py
  migrations/
  scripts/
  app.py
  config.py
  requirements.txt
  .env.example
```

## Regras de negocio (Lead Scoring)

Pontuacao baseada em origem e interesse (urgencia):

- Google Ads = +30
- Instagram = +20
- Facebook = +15
- Site = +25
- Indicado = +10
- Outro = +5

Interesse (urgencia):

- Alta = +40
- Media = +20
- Baixa = +10

Classificacao:

- 0-49 = Frio
- 50-79 = Morno
- 80-100 = Quente

Observacao: o campo "Interesse (urgencia)" no formulario e usado para a regra de scoring.

## Instalacao e execucao

1) Crie o ambiente virtual e instale dependencias:

```
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2) Configure as variaveis de ambiente:

```
copy .env.example .env
```

3) Crie o banco e rode as migracoes:

```
createdb crm_ai
flask db init
flask db migrate -m "init"
flask db upgrade
```

4) Crie o usuario admin:

```
flask create-admin
```

5) Inicie a aplicacao:

```
flask run
```

Acesse: http://127.0.0.1:5000

## Configuracao PostgreSQL

Exemplo de URL:

```
postgresql+psycopg2://postgres:postgres@localhost:5432/crm_ai
```

## Configuracao Ollama

1) Instale o Ollama
2) Baixe o modelo local:

```
ollama pull qwen3:8b
```

3) Garanta que o servico esta ativo em `http://localhost:11434`
4) Ajuste `OLLAMA_URL` e `OLLAMA_MODEL` no `.env`

## Endpoints API

- GET /api/leads
- POST /api/leads
- GET /api/leads/{id}
- PUT /api/leads/{id}
- DELETE /api/leads/{id}
- GET /api/dashboard
- GET /api/reports

## Scripts SQL

- scripts/init_db.sql

## Screenshots simulados

- Dashboard: [Simulado]
- Pipeline: [Simulado]
- Leads: [Simulado]
- Detalhes do Lead: [Simulado]

## Segurança

- Hash de senha com Werkzeug
- Autenticacao Flask-Login
- CSRF com Flask-WTF
- Validacao de formularios com WTForms

## Publicacao no GitHub

```
git init
git add .
git commit -m "feat: crm inteligente"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git
git push -u origin main
```
