# Strivium Link Frontend + Mobile

Este diretório é o app oficial web e mobile do Strivium Link. O mobile usa Capacitor com os projetos nativos em `ios/` e `android/`; não existe um segundo app paralelo.

## Requisitos

- Node.js 22+
- Yarn 1.x
- Ruby 3.2+ para Fastlane/CocoaPods
- Xcode atualizado para builds iOS
- Android Studio/JDK 21 para builds Android

## Ambiente local

```bash
yarn install
cp .env.example .env
yarn dev
```

O projeto local abre em `http://localhost:3000`.

## Build web/mobile

```bash
yarn lint
yarn test
yarn test:contracts:smoke
yarn build
npx cap sync ios
npx cap sync android
```

## Publicação nas lojas

Use os documentos oficiais na raiz do repositório:

- `docs/mobile-release/README.md`
- `docs/mobile-release/app-store-handoff.md`
- `docs/mobile-release/first-release-runbook.md`

Para App Store/TestFlight, o caminho recomendado é o GitHub Actions `Mobile Release` com `release_target=ios`.

Para testes manuais que forçam o app a abrir a versão web remota, existe:

```bash
yarn ios:remote:signin:copy
```

Esse comando é apenas para teste manual. Builds de loja devem usar o export estático do app e `NEXT_PUBLIC_API_URL=https://strivium.link.servidortozato.cloud/api`.
