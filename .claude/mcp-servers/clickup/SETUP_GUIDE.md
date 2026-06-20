# Guia de Configuração - ClickUp MCP Server

## ✅ Status da Instalação

- [x] MCP Server criado
- [x] Configuração `.mcp.json` gerada
- [⏳] Dependências instalando (cryptography compilando)
- [ ] Servidor testado
- [ ] Backlog populado no ClickUp

---

## 📋 Passos para Finalizar a Configuração

### 1. Aguardar Instalação das Dependências

A biblioteca `cryptography` está sendo compilada. Isso pode levar 3-5 minutos.

**Verificar se terminou:**
```bash
ps aux | grep "[p]ython3 -m pip install"
```

Se não retornar nada, a instalação está completa.

**Verificar instalação bem-sucedida:**
```bash
python3 -c "import mcp; print('MCP instalado com sucesso!')"
```

---

### 2. Reiniciar Claude Code

Após a instalação terminar:

1. **Saia da sessão atual** do Claude Code:
   - Pressione `Ctrl+D` ou digite `exit`

2. **Inicie uma nova sessão**:
   ```bash
   claude
   ```

3. **Verifique se o servidor está conectado**:
   ```
   /mcp
   ```

   Você deve ver algo como:
   ```
   Available MCP Servers:
   ✓ clickup - Connected (9 tools)
   ```

---

### 3. Testar Conexão com ClickUp

Dentro do Claude Code, peça para testar:

```
Teste a conexão com o ClickUp usando o MCP server.
Liste os spaces do workspace 90132565680.
```

O Claude irá usar a ferramenta `clickup_list_spaces` automaticamente.

---

### 4. Popular ClickUp com Backlog

Após confirmar que o MCP está funcionando, execute:

```
Agora popule o ClickUp com as sprints e tasks do plano de débitos técnicos.

Estrutura:
- Folder ID base: 901310995817
- Criar 3 folders:
  1. Sprint 1 - Segurança & Compliance
  2. Sprint 2 - Estabilidade & Observabilidade
  3. Backlog - Melhorias Médio Prazo

Dentro de cada sprint, criar lists por prioridade (P0, P1, P2, P3)
e popular com as tasks detalhadas do plano.
```

---

## 🛠️ Troubleshooting

### Erro: "Server not connected"

1. Verifique o caminho no `.mcp.json`:
   ```bash
   cat .mcp.json
   ```

2. Teste o servidor manualmente:
   ```bash
   python3 .claude/mcp-servers/clickup/server.py
   ```

3. Verifique se a API token está correta:
   ```bash
   grep CLICKUP_API_TOKEN .mcp.json
   ```

### Erro: "ModuleNotFoundError: mcp"

Reinstale as dependências:
```bash
cd .claude/mcp-servers/clickup
python3 -m pip install -e . --force-reinstall
```

### Erro de Permissão no ClickUp

Verifique se a API token tem permissões de escrita:
- Acesse: https://app.clickup.com/settings/apps
- Verifique o token `pk_242580334_*`
- Confirme que tem permissão de "Write"

---

## 📖 Próximos Passos

Após configuração bem-sucedida:

1. ✅ Verificar estrutura criada no ClickUp
2. ✅ Revisar tasks e ajustar estimativas se necessário
3. ✅ Atribuir responsáveis
4. ✅ Configurar datas de sprint
5. ✅ Começar desenvolvimento pelo ITEM-001 (CORS)

---

## 🔗 Links Úteis

- **ClickUp Workspace**: https://app.clickup.com/90132565680
- **Folder Base**: https://app.clickup.com/90132565680/v/f/901313952279/901310995817
- **ClickUp API Docs**: https://clickup.com/api/
- **MCP Documentation**: https://modelcontextprotocol.io/

---

## 📝 Arquivos Criados

```
.claude/mcp-servers/clickup/
├── server.py              # Servidor MCP principal
├── pyproject.toml         # Configuração Python
├── README.md              # Documentação do servidor
└── SETUP_GUIDE.md         # Este arquivo

.mcp.json                  # Configuração Claude Code (raiz do projeto)
```

---

**Última atualização**: 2026-06-19
**Status**: Aguardando instalação de dependências
