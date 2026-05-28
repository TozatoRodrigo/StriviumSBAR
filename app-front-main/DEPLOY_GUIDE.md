# Guia de Release Mobile (App Store + Google Play)

Este guia cobre a publicação mobile do Strivium Link com os workflows da raiz:

- `.github/workflows/mobile-ci.yml`
- `.github/workflows/mobile-release.yml`

## 1) Pré-requisitos

- App Apple e app Google Play criados com `br.com.strivium.link`.
- API de produção ativa em `https://api.link.strivium.com.br`.
- Conta demo de revisão pronta (dados fictícios).

## 2) Configurar variáveis e secrets no GitHub

Referência completa:

- [github-secrets-setup.md](../docs/mobile-release/github-secrets-setup.md)

Exemplo de arquivo local para bootstrap:

- [app-front-main/.env.github.release.example](./.env.github.release.example)

## 3) Bootstrap automático (opcional)

Depois de preencher `.env.github.release.local`:

```bash
cd app-front-main
set -a
source .env.github.release.local
set +a
yarn release:github:bootstrap
```

Dry-run:

```bash
cd app-front-main
set -a
source .env.github.release.local
set +a
yarn release:github:bootstrap --dry-run
```

## 4) Disparar release

Pelo GitHub Actions:

- `Actions > Mobile Release > Run workflow`
- `version_name`: ex. `1.0.0`
- `google_play_track`: `internal`

Ou por CLI:

```bash
cd app-front-main
yarn release:github:run --version-name 1.0.0 --google-play-track internal
```

## 5) Validar resultado

Use:

- [release-checklist.md](../docs/mobile-release/release-checklist.md)
- [first-release-runbook.md](../docs/mobile-release/first-release-runbook.md)

Ordem esperada:

1. `Validate CI secrets`
2. `Build web export`
3. `Build Android AAB`
4. `Build iOS IPA`
5. `Deploy Android to Google Play`
6. `Deploy iOS to TestFlight`
