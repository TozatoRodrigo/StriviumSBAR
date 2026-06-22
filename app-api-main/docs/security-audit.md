# Auditoria de Segurança — OWASP Top 10 (2021)

Auditoria de segurança do sistema Strivium (API FastAPI + frontend Next.js/Capacitor),
com foco em conformidade LGPD (Art. 46-50) por se tratar de sistema de saúde com
dados sensíveis de pacientes.

- **Escopo:** `app-api-main` (FastAPI/Python 3.13) e `app-front-main` (Next.js 15 / React 19 / Capacitor).
- **Metodologia:** revisão estática de código (SAST manual) das áreas do OWASP Top 10,
  análise de configuração e dependências. Ver _DAST (OWASP ZAP)_ abaixo para o
  complemento dinâmico recomendado.

## Resumo executivo

| # | Área OWASP | Resultado | Ação |
|---|-----------|-----------|------|
| A01 | Broken Access Control | OK | Auth por JWT + permissões; rate limiting em endpoints sensíveis |
| A02 | Cryptographic Failures | OK | Senhas com bcrypt; `JWT_SECRET` validado (≥32 chars); sem segredos no git |
| A03 | Injection (SQLi/XSS) | OK | ORM parametrizado; React escapa output; sem `dangerouslySetInnerHTML` no app |
| A04 | Insecure Design | OK | Tokens em header `Authorization` (CSRF não aplicável) |
| A05 | Security Misconfiguration | **Corrigido** | **Headers de segurança ausentes na API → middleware adicionado** |
| A06 | Vulnerable Components | OK (monitorado) | `pip-audit` no CI; CVEs pendentes documentados com ignores temporários |
| A07 | Identification & Auth Failures | Observação | Tokens em `localStorage` (tradeoff documentado) |
| A08 | Software & Data Integrity | OK | Sem deserialização insegura (`pickle`/`yaml.load`/`eval`) |
| A09 | Logging & Monitoring | OK | Logs estruturados (JSON); resposta 500 genérica ao cliente |
| A10 | SSRF | OK | Sem requisições a URLs controladas pelo usuário |

## Achados detalhados

### A05 — Security Misconfiguration: headers de segurança ausentes (CORRIGIDO)

**Severidade:** Média · **Status:** Corrigido neste PR

A API não enviava headers de hardening (`X-Content-Type-Options`, `X-Frame-Options`,
`Content-Security-Policy`, `Referrer-Policy`, `Strict-Transport-Security`). Isso
expunha respostas a MIME sniffing, clickjacking e (sem HSTS) downgrade para HTTP.

**Correção:** novo `SecurityHeadersMiddleware`
([app/middlewares/security_headers.py](../app/middlewares/security_headers.py)),
configurável por ambiente, que adiciona a todas as respostas HTTP:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: no-referrer`
- `X-Permitted-Cross-Domain-Policies: none`
- `Content-Security-Policy: default-src 'none'; frame-ancestors 'none'; base-uri 'none'`
  (exceto rotas de docs, para não quebrar o Swagger/ReDoc)
- `Strict-Transport-Security` (opt-in via `SECURITY_HSTS_ENABLED`, habilitado em produção sob HTTPS)

Variáveis: `SECURITY_HEADERS_ENABLED`, `SECURITY_HSTS_ENABLED`, `SECURITY_HSTS_MAX_AGE`,
`SECURITY_CSP`, `SECURITY_REFERRER_POLICY`, `SECURITY_FRAME_OPTIONS`.

### A03 — Injection (SQLi): OK

Todo o acesso a dados usa o ORM SQLModel/SQLAlchemy com queries parametrizadas
(`session.exec(select(Model).where(...))`). Não há SQL cru, `text()` com
interpolação, nem f-strings em queries. **Sem risco de SQLi.**

### A03 — Injection (XSS): OK

O frontend (React 19) escapa automaticamente o conteúdo renderizado em JSX. Não
há uso de `dangerouslySetInnerHTML`, `innerHTML`, `eval` ou `document.write` no
código de aplicação (`src/`) — as únicas ocorrências estão em chunks gerados pelo
próprio Next.js (script de tema). **Sem vetor de XSS introduzido pela aplicação.**

### A04 — CSRF: não aplicável (por design)

A autenticação usa `Authorization: Bearer <token>` (ver `src/api/axios.ts`), sem
cookies de sessão e sem `withCredentials`. Ataques CSRF dependem do envio
automático de cookies pelo navegador; como o token só é acessível via JavaScript
da própria origem e enviado explicitamente em header, **CSRF não se aplica**.
Tokens CSRF só seriam necessários se a autenticação migrasse para cookies.

### A07 — Tokens em `localStorage` (observação)

**Severidade:** Baixa/Informativa · **Status:** Documentado (sem mudança neste PR)

Os tokens de acesso/refresh são persistidos em `localStorage`
(`src/hooks/usePersistTokens.ts`, contexts de auth). Isso é prática comum para
SPA + app Capacitor, mas expõe os tokens a roubo em caso de XSS. Mitigações já
presentes: ausência de vetores de XSS (A03) e CSP restritiva.

**Recomendação (fora do escopo deste PR):** avaliar tokens de acesso de curta
duração + rotação de refresh (já há `REFRESH_TOKEN_STRICT_MODE`), e considerar
`httpOnly` cookies caso a arquitetura web evolua (exigiria então proteção CSRF).

### A06 — Componentes vulneráveis: monitorado

O CI já roda `pip-audit` no job _Security audit_. Há CVEs conhecidos pendentes
(cryptography, python-multipart, starlette) com `--ignore-vuln` temporários e
documentados, aguardando versões compatíveis com o framework. **Revisar
periodicamente.**

### A09 — Exposição de dados em logs/erros: OK

- Respostas de erro ao cliente são genéricas: o handler catch-all retorna apenas
  `{"message": "Internal server error"}` com status 500, sem stack trace.
- Logs são estruturados em JSON (`GCPJsonFormatter`). Não há logging de senhas,
  tokens ou `Authorization`. **Recomendação:** evitar logar corpos de request em
  endpoints sensíveis (mantido como diretriz no checklist de PR).

## DAST (OWASP ZAP) — complemento recomendado

A revisão estática acima não substitui um scan dinâmico. Recomenda-se rodar o
**OWASP ZAP** (baseline scan) contra um ambiente de _staging_ a cada release:

```bash
docker run --rm -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t https://staging-api.strivium.com.br -r zap-report.html
```

Os headers adicionados neste PR devem eliminar os alertas de _missing security
headers_ que um baseline scan tipicamente reporta.

## Conformidade LGPD

- **Art. 46 (segurança):** rate limiting, headers de segurança, senhas com bcrypt,
  TLS/HSTS em produção, controle de acesso por permissões.
- **Art. 47-49 (boas práticas/governança):** este relatório + o
  [checklist de segurança para PRs](./security-checklist.md) institucionalizam a
  revisão contínua.

## Itens da história

- [x] Executar scan de segurança — revisão estática (SAST) completa; ZAP/DAST documentado para staging
- [x] Revisar SQLi — ORM parametrizado, sem SQL cru
- [x] Revisar XSS — React escapa output; sem `dangerouslySetInnerHTML`
- [x] Revisar CSRF — não aplicável (Bearer token em header), documentado
- [x] Revisar exposição de dados em logs/erros — 500 genérico, logs estruturados
- [x] Revisar config de segurança (CORS, headers) — CORS já restrito; headers adicionados
- [x] Documentar vulnerabilidades e correções — este documento
- [x] Criar checklist de segurança para PRs — [security-checklist.md](./security-checklist.md)
