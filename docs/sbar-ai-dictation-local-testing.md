# Ditado SBAR com Ollama - Teste local

## Requisitos

- Frontend com `NEXT_PUBLIC_EXPERIMENTAL_SBAR_AI_DICTATION=true`.
- Backend com `SBAR_AI_ENABLED=true`.
- Ollama instalado na máquina que executa a API.
- Modelo local baixado:

```bash
ollama pull llama3.2:3b
```

## Variáveis de ambiente

No backend:

```env
SBAR_AI_ENABLED=true
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
OLLAMA_TIMEOUT_SECONDS=30
```

No frontend:

```env
NEXT_PUBLIC_EXPERIMENTAL_SBAR_AI_DICTATION=true
```

## Como testar

1. Inicie o Ollama e confirme que o modelo responde:

```bash
ollama run llama3.2:3b
```

2. Rode API, banco e front como no fluxo local do projeto.
3. Acesse uma internação e abra `Registrar visita`.
4. Dite ou digite o texto bruto em `Ditado livre`.
5. Clique em `Organizar em SBAR`.
6. Revise os campos preenchidos, warnings e informações ausentes.
7. Marque `Revisei e confirmo o rascunho gerado pela IA`.
8. Salve a evolução.

## Teste de capacidade da VPS

Antes de liberar em produção, medir:

```bash
free -h
nproc
df -h
```

Critério mínimo para piloto:

- 4 GB de RAM com folga real.
- `OLLAMA_NUM_PARALLEL=1`.
- Feature flag ativa apenas para usuários de teste.

Critério recomendado:

- 8 GB de RAM.
- 4 vCPU.
- Latência P95 aceitável com 10 transcrições reais anonimizadas.

Se a VPS tiver 1-2 GB de RAM, não rode Ollama nela. Use apenas ditado/manual ou hospede a IA em outra máquina.
