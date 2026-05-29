# Strivium Link Mobile Release

Este diretório é o ponto de entrada para desenvolvedores que vão preparar TestFlight, App Store e Google Play.

## Status atual

- App oficial: `app-front-main`
- Backend oficial: `app-api-main`
- Bundle ID / package: `br.com.strivium.link`
- Nome público: `Strivium Link`
- Web atual: `https://strivium.link.servidortozato.cloud/signin`
- API atual para builds mobile: `https://strivium.link.servidortozato.cloud/api`
- CI/CD oficial: `.github/workflows/`

## Ordem recomendada

1. Leia o handoff de App Store: [app-store-handoff.md](./app-store-handoff.md)
2. Configure os secrets: [github-secrets-setup.md](./github-secrets-setup.md)
3. Rode o primeiro release interno: [first-release-runbook.md](./first-release-runbook.md)
4. Complete a checklist: [release-checklist.md](./release-checklist.md)
5. Preencha privacidade e metadados:
   - [privacy-data-map.md](./privacy-data-map.md)
   - [store-metadata.md](./store-metadata.md)
   - [screenshots-guide.md](./screenshots-guide.md)

## Regras importantes

- Não criar outro app mobile paralelo. O Capacitor já está em `app-front-main/ios` e `app-front-main/android`.
- Não usar `CAPACITOR_SERVER_URL` em build de loja. Essa variável serve apenas para teste manual remoto.
- Para App Store/TestFlight, use o GitHub Actions `Mobile Release` com `release_target=ios`.
- Para Google Play, use `release_target=android`.
- Para release completo das duas lojas, use `release_target=all`.
