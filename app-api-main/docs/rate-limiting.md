# Rate Limiting na API Strivium

## Visão Geral

A API Strivium possui rate limiting implementado usando a biblioteca `slowapi`, que ajuda a proteger contra abuso da API e ataques de negação de serviço (DoS).

## Limites Padrão

Por padrão, todos os endpoints da API possuem os seguintes limites:

- **100 requisições por minuto** por endereço IP
- **1000 requisições por hora** por endereço IP

## Como Funciona

O rate limiting identifica os clientes pelo endereço IP remoto e rastreia o número de requisições dentro de janelas de tempo específicas. Os headers informativos `X-RateLimit-*` são emitidos em todas as respostas (configuração `headers_enabled=True`). Quando um cliente excede o limite:

1. A API retorna o status HTTP `429 Too Many Requests`
2. O header `Retry-After` informa quando o cliente pode tentar novamente
3. Headers adicionais como `X-RateLimit-Limit`, `X-RateLimit-Remaining` e `X-RateLimit-Reset` fornecem informações sobre o limite

## Limites Específicos por Endpoint

### Endpoints de Autenticação

**`POST /auth/v1/login`** - Login de usuário
- **Limite:** 5 requisições por minuto
- **Motivo:** Proteção contra ataques de força bruta
- **Proteção adicional:** Cloudflare Turnstile CAPTCHA

**`POST /auth/v1/tenant`** - Autenticação de tenant
- **Limite:** 10 requisições por minuto
- **Motivo:** Limitar trocas rápidas de contexto de tenant

## Uso em Rotas Específicas

### Aplicar Limite Personalizado a uma Rota

Para aplicar um limite diferente do padrão a uma rota específica, use o decorator `@limiter.limit()`:

```python
from fastapi import APIRouter, Request
from app.core.rate_limiter import limiter

router = APIRouter()

@router.post("/endpoint")
@limiter.limit("5/minute")  # Apenas 5 requisições por minuto
async def endpoint(request: Request, ...):
    # Lógica do endpoint
    ...
```

⚠️ **IMPORTANTE:** O parâmetro `request: Request` é obrigatório quando usando o decorator `@limiter.limit()`.

### Exemplos de Limites

```python
# 10 requisições por minuto
@limiter.limit("10/minute")

# 5 requisições por segundo
@limiter.limit("5/second")

# 1000 requisições por hora
@limiter.limit("1000/hour")

# 100 requisições por dia
@limiter.limit("100/day")

# Múltiplos limites (aplica o mais restritivo)
@limiter.limit("10/second;100/minute;1000/hour")
```

### Isentar uma Rota do Rate Limiting

Para isentar completamente uma rota do rate limiting:

```python
from slowapi import Limiter
from app.core.rate_limiter import limiter

@router.get("/health")
@limiter.exempt  # Esta rota não terá rate limiting
async def health_check():
    return {"status": "healthy"}
```

## Configuração

A configuração do rate limiting está centralizada em:

- **Arquivo:** `app/core/rate_limiter.py`
- **Configuração no app:** `app/main.py`
- **Variáveis de ambiente:** `app/core/environment.py`

Toda a configuração é feita por variáveis de ambiente, sem necessidade de
alterar código:

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `RATE_LIMIT_ENABLED` | `true` | Liga/desliga o rate limiting globalmente. |
| `RATE_LIMIT_STORAGE_URI` | `memory://` | Backend de armazenamento. Use uma URL Redis em produção. |
| `RATE_LIMIT_DEFAULT` | `100/minute;1000/hour` | Limites globais (lista separada por `;`). |
| `RATE_LIMIT_AUTH_LOGIN` | `5/minute` | Limite do endpoint `POST /auth/v1/login`. |
| `RATE_LIMIT_AUTH_TENANT` | `10/minute` | Limite do endpoint `POST /auth/v1/tenant`. |

### Modificar Limites Padrão

Para alterar os limites, basta ajustar as variáveis de ambiente. Por exemplo,
no `.env`:

```bash
RATE_LIMIT_DEFAULT=200/minute;2000/hour
RATE_LIMIT_AUTH_LOGIN=10/minute
```

### Usar Redis para Armazenamento Distribuído

Em produção com múltiplas instâncias da API, o armazenamento em memória não é
suficiente (cada instância teria a sua própria contagem). Aponte
`RATE_LIMIT_STORAGE_URI` para o Redis:

```bash
RATE_LIMIT_STORAGE_URI=redis://strivium-redis:6379/0
```

O `docker-compose.yaml` já provê um serviço `redis` (`strivium-redis`) para
desenvolvimento local. A dependência `redis` já está declarada em
`pyproject.toml`, portanto nenhuma alteração de código é necessária — apenas
configure a variável de ambiente.

## Resposta ao Atingir o Limite

Quando um cliente excede o limite, a resposta será:

```json
{
  "error": "Rate limit exceeded: 100 per 1 minute"
}
```

Com os seguintes headers HTTP:

```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1234567890
Retry-After: 60
```

## Melhores Práticas

1. **Endpoints de Autenticação**: Aplique limites mais restritos (ex: 5/minuto) para prevenir ataques de força bruta
2. **Endpoints de Leitura**: Podem ter limites mais generosos
3. **Endpoints de Escrita**: Devem ter limites moderados para prevenir spam
4. **Webhooks/Callbacks**: Considere isentar ou aplicar limites muito altos
5. **Health Checks**: Devem ser isentos para não afetar monitoramento

## Monitoramento

Para monitorar rate limiting:

```python
from slowapi import Limiter

# Logs automáticos são gerados quando um limite é atingido
# Verifique os logs da aplicação para mensagens do tipo:
# "Rate limit exceeded for IP: x.x.x.x"
```

## Testes

Para testar o rate limiting localmente:

O comportamento de throttling é coberto por um teste isolado e determinístico
(`app/tests/feature/test_rate_limiting.py`), que cria uma aplicação própria com
o limiter habilitado — assim não interfere nas demais suítes. No ambiente de
teste o rate limiting global fica desativado (`RATE_LIMIT_ENABLED=false` em
`.env.testing`).

```bash
# Execute os testes específicos de rate limiting
pytest app/tests/feature/test_rate_limiting.py -v

# Ou teste manualmente com curl
for i in {1..10}; do
  curl -X POST http://localhost:8000/auth/v1/login \
    -H "Content-Type: application/json" \
    -H "x-turnstile-token: test-token" \
    -d '{"login":"test@test.com","password":"test123"}';
done
```

## Considerações de Segurança

- O rate limiting usa o IP do cliente para identificação
- Em produção atrás de proxy/load balancer, configure corretamente os headers `X-Forwarded-For`
- Considere implementar autenticação baseada em API key para limites por usuário ao invés de IP
- Rate limiting é uma camada de defesa, mas não substitui autenticação e autorização adequadas

## Integração com Sistemas Existentes

O rate limiting foi integrado sem afetar funcionalidades existentes:

- ✅ **JWT Authentication** - Mantida intacta
- ✅ **CORS Configuration** - Preservada
- ✅ **Turnstile CAPTCHA** - Continua funcionando no login
- ✅ **Exception Handlers** - Não alterados
- ✅ **Middlewares Existentes** - SetTimezoneMiddleware preservado

## Troubleshooting

### Erro: "Missing request parameter"

Se você receber este erro ao adicionar `@limiter.limit()` a uma função, certifique-se de adicionar o parâmetro `request: Request`:

```python
# ❌ Errado
@limiter.limit("10/minute")
def my_endpoint(data: MyDTO):
    ...

# ✅ Correto
@limiter.limit("10/minute")
def my_endpoint(request: Request, data: MyDTO):
    ...
```

### Rate limiting não está funcionando

1. Verifique se `SlowAPIMiddleware` está adicionado em `app/main.py`
2. Verifique se `app.state.limiter = limiter` está configurado
3. Verifique se o exception handler `RateLimitExceeded` está registrado
4. Para endpoints específicos, certifique-se de importar o limiter: `from app.core.rate_limiter import limiter`

## Referências

- [SlowAPI Documentation](https://slowapi.readthedocs.io/)
- [FastAPI Rate Limiting Guide](https://fastapi.tiangolo.com/advanced/middleware/)
