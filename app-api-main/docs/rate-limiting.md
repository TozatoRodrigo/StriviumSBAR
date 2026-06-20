# Rate Limiting na API Strivium

## Visão Geral

A API Strivium possui rate limiting implementado usando a biblioteca `slowapi`, que ajuda a proteger contra abuso da API e ataques de negação de serviço (DoS).

## Limites Padrão

Por padrão, todos os endpoints da API possuem os seguintes limites:

- **100 requisições por minuto** por endereço IP
- **1000 requisições por hora** por endereço IP

## Como Funciona

O rate limiting identifica os clientes pelo endereço IP remoto e rastreia o número de requisições dentro de janelas de tempo específicas. Quando um cliente excede o limite:

1. A API retorna o status HTTP `429 Too Many Requests`
2. O header `Retry-After` informa quando o cliente pode tentar novamente
3. Headers adicionais como `X-RateLimit-Limit` e `X-RateLimit-Remaining` fornecem informações sobre o limite

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

### Modificar Limites Padrão

Para alterar os limites padrão da API, edite o arquivo `app/core/rate_limiter.py`:

```python
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200/minute", "2000/hour"],  # Novos limites
    storage_uri="memory://",
)
```

### Usar Redis para Armazenamento Distribuído

Para ambientes de produção com múltiplas instâncias, recomenda-se usar Redis:

```python
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute", "1000/hour"],
    storage_uri="redis://localhost:6379",  # URL do Redis
)
```

Para usar Redis, adicione a dependência:
```toml
dependencies = [
    ...
    "redis (>=5.2.2,<6.0.0)",
]
```

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
