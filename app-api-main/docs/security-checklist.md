# Checklist de Segurança para Pull Requests

Revisão rápida baseada no OWASP Top 10 e na LGPD. Marque os itens aplicáveis ao
PR. Itens não aplicáveis devem ser marcados como `N/A`. Ver a
[auditoria de segurança](./security-audit.md) para o racional.

## Controle de acesso (A01)
- [ ] Novos endpoints exigem autenticação e a permissão correta (não confiar só no frontend).
- [ ] Não há _IDOR_: o usuário só acessa recursos do próprio tenant/escopo.
- [ ] Endpoints sensíveis (auth, dados de paciente) têm rate limiting adequado.

## Criptografia e segredos (A02)
- [ ] Nenhum segredo (chaves, senhas, tokens) commitado — usar `.env`/variáveis de ambiente.
- [ ] Senhas sempre com hash (bcrypt); nunca em texto puro.
- [ ] Dados sensíveis trafegam só sobre HTTPS.

## Injeção (A03)
- [ ] Queries via ORM parametrizado; sem SQL cru com interpolação de strings.
- [ ] Frontend não usa `dangerouslySetInnerHTML` com conteúdo não sanitizado.
- [ ] Inputs validados por DTO/schema (Pydantic) antes do uso.

## Design e CSRF (A04)
- [ ] Auth permanece via header `Authorization: Bearer` (não introduzir auth por cookie sem proteção CSRF).
- [ ] Operações destrutivas exigem confirmação/autorização explícita.

## Configuração (A05)
- [ ] Não afrouxar o CORS (`allow_origins` deve listar origens explícitas, nunca `*` com credenciais).
- [ ] Não desabilitar os headers de segurança nem o rate limiting sem justificativa.
- [ ] `ENABLE_DOCS=false` em produção.

## Dependências (A06)
- [ ] Novas dependências verificadas; `pip-audit` (API) / `npm audit` (front) sem CVEs críticos não tratados.
- [ ] Lockfiles atualizados (`poetry.lock` + `uv.lock`).

## Autenticação (A07)
- [ ] Fluxos de login/refresh/logout testados; tokens com expiração e rotação de refresh.
- [ ] Sem expor tokens em logs, URLs ou mensagens de erro.

## Integridade (A08)
- [ ] Sem deserialização insegura (`pickle`, `yaml.load`, `eval`, `new Function`).

## Logging e monitoramento (A09)
- [ ] Erros retornam mensagem genérica ao cliente (sem stack trace/dados sensíveis).
- [ ] Logs não contêm PII de paciente, senhas, tokens ou `Authorization`.
- [ ] Eventos de segurança relevantes (login falho, rate limit) são logados.

## SSRF e uploads (A10)
- [ ] Requisições externas não usam URLs controladas pelo usuário sem allowlist.
- [ ] Uploads validam tipo/tamanho (`UPLOAD_ALLOWED_*`, `UPLOAD_MAX_FILE_SIZE_MB`).

## LGPD
- [ ] A mudança não expõe dados pessoais/sensíveis de pacientes além do necessário.
- [ ] Acesso a dados de paciente é registrado e restrito ao escopo do usuário.
