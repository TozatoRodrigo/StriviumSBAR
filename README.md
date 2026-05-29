# Strivium Platform Repository

Monorepo segmentado para facilitar operação de produto web, backend e publicação mobile (App Store + Google Play).

## Estrutura

```txt
Github_Strivium/
  .github/workflows/          # CI/CD centralizado
  docs/mobile-release/        # runbooks e checklist de publicação
  app-front-main/             # frontend web + projeto mobile Capacitor (ios/android)
  app-api-main/               # backend FastAPI
```

## Onde cada time atua

- Web e mobile: `app-front-main`
- Backend/API: `app-api-main`
- Pipelines GitHub Actions: `.github/workflows`
- Procedimento de loja: `docs/mobile-release`

## Workflows oficiais

- `mobile-ci.yml`: lint, testes e build do front.
- `mobile-release.yml`: build/sign/deploy Android (AAB) e iOS (IPA/TestFlight).
- `api-ci.yml`: testes, lint e auditoria do backend.

> Observação: workflows em subpastas (`app-front-main/.github` e `app-api-main/.github`) foram descontinuados. O padrão oficial é usar apenas `.github/workflows` na raiz.

## Handoff para publicação nas lojas

Comece por aqui ao enviar para os desenvolvedores:

1. Visão geral do release mobile:
   - `docs/mobile-release/README.md`
2. Handoff específico para App Store/TestFlight:
   - `docs/mobile-release/app-store-handoff.md`
3. Configurar secrets/variables:
   - `docs/mobile-release/github-secrets-setup.md`
4. Validar setup inicial:
   - `docs/mobile-release/first-release-runbook.md`
5. Executar release checklist:
   - `docs/mobile-release/release-checklist.md`
6. Publicar primeiro em:
   - Google Play `internal`
   - TestFlight internal

Configuração atual de produção para o app mobile:

- App/bundle id: `br.com.strivium.link`
- Web atual: `https://strivium.link.servidortozato.cloud/signin`
- API atual para builds mobile: `https://strivium.link.servidortozato.cloud/api`
- Build de loja: não usar `CAPACITOR_SERVER_URL`; esse modo é só para teste manual remoto.

## Comandos rápidos (a partir da raiz)

Frontend:

```bash
cd app-front-main
yarn lint
yarn test
yarn test:contracts:smoke
yarn build
```

Backend:

```bash
cd app-api-main
APP_ENV=testing poetry run pytest
poetry run ruff check app
poetry run ruff format --check app
```
