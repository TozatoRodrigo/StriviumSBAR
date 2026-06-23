# Logs de Auditoria (LGPD)

Sistema de _audit logs_ para rastrear ações sensíveis e garantir conformidade
com a LGPD (Art. 46 e 48 — segurança e rastreabilidade de acesso a dados
pessoais).

## Visão geral

Cada ação sensível gera um registro **imutável** em `audit_logs` contendo
**quem** (usuário/tenant), **o quê** (ação/recurso), **quando** (timestamp),
**de onde** (IP, user-agent) e o **resultado** (status HTTP). Tudo é capturado
automaticamente por um middleware, sem necessidade de alterar cada endpoint.

## Eventos auditados

Definidos em `app/enums/models/audit_enums.py` e mapeados para rotas em
`app/middlewares/audit_middleware.py`:

| Evento | Rota | Ação |
|--------|------|------|
| Login | `POST /auth/v1/login` | `login` / `login_failed` |
| Logout | `POST /auth/v1/logout` | `logout` |
| Visualizar paciente | `GET /patient/v1/patients/{id}` | `view:patient` |
| Criar/atualizar paciente | `POST/PUT /patient/v1/patients` | `create/update:patient` |
| Visualizar internação | `GET /hospitalization/v1/hospitalizations/{id}` | `view:hospitalization` |
| CRUD de internação | `POST/PUT .../hospitalizations` | `create/update:hospitalization` |
| Ação de internação | `POST .../hospitalization-actions` | `create:hospitalization_action` |
| SBAR | `POST /api/sbar/extract` | `create:sbar` |
| Usuários do tenant | `POST /tenant-user/v1/tenant-users` | `create:tenant_user` |

Para auditar uma nova rota, basta adicionar uma entrada em `_AUDITED_ROUTES`.

## Dados registrados

Colunas de `audit_logs`: `user_id`, `tenant_id`, `action`, `resource_type`,
`resource_id`, `method`, `path`, `status_code`, `ip_address`, `user_agent`,
`changes` (JSON `{"before", "after"}`), `created_at`.

> **Minimização de dados (LGPD):** o middleware registra apenas **metadados de
> acesso** (quem/o quê/quando/de onde), **não** o conteúdo de dados pessoais.
> Diffs `antes/depois` campo a campo são opcionais e gravados por use cases que
> chamam `AuditLogService.record(..., changes=...)` explicitamente — evitando
> duplicar PII de pacientes no log.

## Como funciona

`AuditLogMiddleware` (registrado em `app/main.py`):

1. Casa o método + path da requisição com `_AUDITED_ROUTES`.
2. Executa a requisição e captura o status da resposta.
3. Decodifica o JWT (best-effort) para obter `user_id`/`tenant_id`.
4. Extrai IP (`X-Forwarded-For` → cliente), user-agent e `resource_id` do path.
5. Persiste via `AuditLogService.record` em sessão própria.

O registro acontece **após** a resposta e **nunca** quebra a requisição:
falhas de auditoria são logadas e suprimidas.

## Consulta (endpoint admin)

```
GET /audit/v1/logs
```

- **Permissão:** `read:audit_log` (concedida ao papel **admin**).
- **Filtros (query):** `user_id`, `action`, `resource_type`, `start_date`,
  `end_date`, `page`, `limit` (máx. 100).
- **Resposta:** paginada (`data`, `total`, `page`, `limit`, `total_pages`).

Exemplo:

```bash
curl -H "Authorization: Bearer <tenant-token>" \
  "https://api.strivium.com.br/audit/v1/logs?action=login_failed&page=1&limit=20"
```

## Retenção (LGPD)

A LGPD exige rastreabilidade; a retenção padrão é **180 dias (~6 meses)**,
configurável por `AUDIT_LOG_RETENTION_DAYS`. A limpeza é feita por um script
idempotente, ideal para um cron diário:

```bash
poetry run python -m app.scripts.purge_audit_logs
```

Remove entradas mais antigas que a janela de retenção. **Não** reduza a janela
abaixo do mínimo legal de rastreabilidade.

## Configuração

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `AUDIT_LOG_ENABLED` | `true` | Liga/desliga o registro de auditoria. |
| `AUDIT_LOG_RETENTION_DAYS` | `180` | Janela de retenção em dias (≥180). |

## Migração

A tabela é criada pela migration `d4f1a2b3c5e7_create_audit_logs_table.py`:

```bash
poetry run alembic upgrade head
```

## Arquivos principais

- `app/models/audit_log.py` — modelo da tabela
- `app/middlewares/audit_middleware.py` — captura automática
- `app/services/audit/audit_log_service.py` — serviço de gravação
- `app/modules/audit/` — endpoint admin (controller/rotas/use case/DTOs)
- `app/scripts/purge_audit_logs.py` — retenção
- `app/tests/feature/test_audit_logs.py` — testes
