# Descrição

<!-- O que muda e por quê. Link para a tarefa/história. -->

## Tipo de mudança

- [ ] Bug fix
- [ ] Nova funcionalidade
- [ ] Refatoração
- [ ] Documentação / chore

## Como testar

<!-- Passos para validar a mudança. -->

## Checklist

- [ ] Testes automatizados cobrindo a mudança
- [ ] Lint e format passando
- [ ] Documentação atualizada quando necessário

## Checklist de segurança

Revisão obrigatória para mudanças que tocam autenticação, dados de paciente,
endpoints, dependências ou configuração. Ver
[`docs/security-checklist.md`](../app-api-main/docs/security-checklist.md).

- [ ] Controle de acesso: endpoints exigem auth + permissão; sem IDOR
- [ ] Sem segredos commitados; dados sensíveis só sobre HTTPS
- [ ] Sem injeção: ORM parametrizado; output escapado no frontend
- [ ] CORS/headers de segurança e rate limiting preservados
- [ ] Erros/logs não expõem dados sensíveis (PII, tokens, stack traces)
- [ ] Dependências auditadas e lockfiles atualizados
- [ ] LGPD: a mudança não expõe dados de paciente além do necessário
- [ ] N/A — esta mudança não tem impacto de segurança
