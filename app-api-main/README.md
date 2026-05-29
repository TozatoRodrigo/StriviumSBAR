# Strivium API

API para o sistema Strivium — gestão de internações hospitalares com suporte a SBAR e ditado por IA.

## Requisitos

- Python 3.12+
- Poetry
- PostgreSQL (produção) / SQLite (testes)

## Setup Local

```bash
cp .env.example .env
# Edite o .env com seus valores (obrigatório: JWT_SECRET, DB_*)
poetry install
poetry run alembic upgrade head
poetry run python -m app.seed
poetry run uvicorn app.main:app --reload --port 55000
```

## Variáveis de Ambiente

### Obrigatórias

| Variável | Descrição |
|---|---|
| `JWT_SECRET` | Segredo JWT com no mínimo 32 caracteres. **Gerar um valor aleatório único para cada ambiente.** |
| `DB_HOST` | Host do banco de dados |
| `DB_PORT` | Porta do banco de dados |
| `DB_NAME` | Nome do banco de dados |
| `DB_USER` | Usuário do banco de dados |
| `DB_PASSWORD` | Senha do banco de dados |

### Opcionais

| Variável | Default | Descrição |
|---|---|---|
| `DB_DRIVER` | `postgresql` | Driver do banco |
| `DB_DEBUG` | `false` | Log SQL |
| `APP_URL` | `http://localhost:55000` | URL base da aplicação |
| `CORS_ALLOWED_ORIGINS` | - | Origins separadas por vírgula |
| `ENABLE_DOCS` | `false` | Habilita Swagger/ReDoc |
| `FILESYSTEM_DRIVER` | `local` | `local` ou `s3` |
| `UPLOAD_MAX_FILE_SIZE_MB` | `20` | Tamanho máximo de upload (MB) |
| `UPLOAD_ALLOWED_EXTENSIONS` | `png,jpg,jpeg,...` | Extensões permitidas |
| `UPLOAD_ALLOWED_MIME_TYPES` | `image/png,...` | MIME types permitidos |
| `MAIL_HOST` | - | Servidor SMTP |
| `MAIL_PORT` | - | Porta SMTP |
| `MAIL_USERNAME` | - | Usuário SMTP |
| `MAIL_PASSWORD` | - | Senha SMTP |
| `MAIL_FROM` | - | Email de remetente |
| `MAIL_USE_TLS` | `true` | Usar TLS no SMTP |
| `TURNSTILE_ENABLED` | `true` | Proteção Cloudflare Turnstile |
| `CLOUDFLARE_TURNSTILE_SECRET` | - | Secret do Turnstile |
| `SBAR_AI_ENABLED` | `false` | Extração SBAR por IA |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | URL do Ollama |
| `OLLAMA_MODEL` | `llama3.2:3b` | Modelo Ollama |
| `OLLAMA_TIMEOUT_SECONDS` | `30` | Timeout do Ollama |

## Testes

```bash
APP_ENV=testing poetry run pytest
```

## Lint

```bash
poetry run ruff check app
poetry run ruff format --check app
```

## Security Audit

```bash
poetry run python -m pip install pip-audit
poetry run python -m pip_audit --cache-dir /tmp/pip-audit-cache
```

## Checklist de Produção

- [ ] `JWT_SECRET` gerado aleatoriamente (mínimo 32 chars, diferente do `.env.example`)
- [ ] `CORS_ALLOWED_ORIGINS` configurado com as origins corretas (sem wildcard)
- [ ] `ENABLE_DOCS=false` (desabilitar Swagger em produção)
- [ ] `FILESYSTEM_DRIVER=s3` configurado com credenciais AWS
- [ ] `MAIL_*` configurado com servidor SMTP real com TLS
- [ ] `TURNSTILE_ENABLED=true` com secret válido
- [ ] Banco de dados com credenciais dedicadas (não root/admin)
- [ ] TLS/HTTPS no proxy reverso
- [ ] Backups automáticos do banco de dados
