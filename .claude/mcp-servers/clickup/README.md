# ClickUp MCP Server

MCP (Model Context Protocol) server para integração com ClickUp API.

## Funcionalidades

- ✅ Listar workspaces, spaces, folders e lists
- ✅ Criar folders e lists
- ✅ Criar tasks com descrição detalhada, prioridade, tags e estimativas
- ✅ Adicionar comentários em tasks
- ✅ Suporte completo à API v2 do ClickUp

## Instalação

### 1. Instalar dependências

```bash
cd .claude/mcp-servers/clickup
pip install -e .
```

### 2. Configurar API Token

O token deve ser configurado no arquivo de configuração MCP do Claude Code.

## Ferramentas Disponíveis

### `clickup_list_workspaces`
Lista todos os workspaces (teams) acessíveis.

### `clickup_list_spaces`
Lista todos os spaces em um workspace.

### `clickup_list_folders`
Lista todas as folders em um space.

### `clickup_get_folder_details`
Obtém detalhes de uma folder específica.

### `clickup_list_lists`
Lista todas as lists em uma folder.

### `clickup_create_folder`
Cria uma nova folder em um space.

**Parâmetros:**
- `space_id` (string): ID do space
- `name` (string): Nome da folder

### `clickup_create_list`
Cria uma nova list em uma folder.

**Parâmetros:**
- `folder_id` (string): ID da folder
- `name` (string): Nome da list
- `content` (string, opcional): Descrição da list
- `priority` (integer, opcional): 1=urgent, 2=high, 3=normal, 4=low

### `clickup_create_task`
Cria uma task com informações detalhadas.

**Parâmetros:**
- `list_id` (string): ID da list
- `name` (string): Nome da task
- `description` (string, opcional): Descrição detalhada (Markdown)
- `priority` (integer, opcional): 1=urgent, 2=high, 3=normal, 4=low
- `tags` (array, opcional): Lista de tags
- `time_estimate` (integer, opcional): Estimativa em horas

### `clickup_add_task_comment`
Adiciona comentário em uma task.

**Parâmetros:**
- `task_id` (string): ID da task
- `comment` (string): Texto do comentário (Markdown)

## Estrutura de Prioridades

- **1**: 🔴 Urgent (P0/Blocker)
- **2**: 🟠 High (P1)
- **3**: 🟡 Normal (P2)
- **4**: 🟢 Low (P3)

## Exemplo de Uso

```python
# Criar folder para Sprint 1
clickup_create_folder(
    space_id="901313952279",
    name="Sprint 1 - Segurança & Compliance"
)

# Criar list dentro da folder
clickup_create_list(
    folder_id="<folder_id>",
    name="P0: Segurança Imediata",
    content="Tasks críticas de segurança que bloqueiam produção"
)

# Criar task detalhada
clickup_create_task(
    list_id="<list_id>",
    name="ITEM-001: Restringir CORS para Domínios Permitidos",
    description="## Objetivo\\n\\nEliminar vulnerabilidade...",
    priority=1,
    tags=["security", "blocker", "lgpd"],
    time_estimate=1
)
```

## Troubleshooting

### Erro de autenticação
Verifique se o `CLICKUP_API_TOKEN` está configurado corretamente no MCP config.

### Erro ao criar tasks
- Verifique se os IDs (folder_id, list_id) estão corretos
- Confirme que você tem permissões no workspace
