# App Store Handoff

Guia objetivo para desenvolvedores publicarem o Strivium Link no TestFlight e, depois, na Apple App Store.

## Escopo

- Diretório do app: `app-front-main`
- Projeto iOS: `app-front-main/ios/App/App.xcworkspace`
- Scheme: `App`
- Bundle ID: `br.com.strivium.link`
- Nome do app: `Strivium Link`
- API de produção atual: `https://strivium.link.servidortozato.cloud/api`

## O que já está pronto no repositório

- Capacitor 8 com `ios/` e `android/` versionados.
- `PrivacyInfo.xcprivacy` em `ios/App/App/PrivacyInfo.xcprivacy`.
- Permissões de microfone e reconhecimento de fala no `Info.plist`.
- Fastlane em `app-front-main/fastlane/Fastfile`.
- Workflow de release em `.github/workflows/mobile-release.yml`.
- Workflow de CI mobile em `.github/workflows/mobile-ci.yml`.
- Build Docker de produção com Node 22.
- Documentação de privacidade, metadados e screenshots em `docs/mobile-release/`.

## O que o desenvolvedor precisa configurar

No Apple Developer/App Store Connect:

- Criar/confirmar App ID com bundle `br.com.strivium.link`.
- Criar app no App Store Connect com o mesmo bundle ID.
- Criar App Store Connect API Key.
- Ter uma conta Apple Developer ativa.
- Preparar política de privacidade pública.
- Preparar conta demo de revisão com dados fictícios.

No GitHub:

- Configurar a variável `NEXT_PUBLIC_API_URL=https://strivium.link.servidortozato.cloud/api`.
- Configurar a variável `NEXT_PUBLIC_TURNSTILE_SITE_KEY`.
- Configurar os secrets de iOS listados em [github-secrets-setup.md](./github-secrets-setup.md):
  - `MATCH_GIT_URL`
  - `MATCH_PASSWORD`
  - `MATCH_GIT_PRIVATE_KEY` ou `MATCH_GIT_PRIVATE_KEY_BASE64` ou `MATCH_GIT_BASIC_AUTHORIZATION`
  - `APP_STORE_CONNECT_API_KEY_KEY_ID`
  - `APP_STORE_CONNECT_API_KEY_ISSUER_ID`
  - `APP_STORE_CONNECT_API_KEY_KEY`

## Como gerar TestFlight pelo GitHub Actions

1. Abra `Actions`.
2. Selecione `Mobile Release`.
3. Clique em `Run workflow`.
4. Preencha:
   - `version_name`: por exemplo `1.0.0`
   - `release_target`: `ios`
   - `google_play_track`: pode deixar `internal`; esse campo só é usado em Android.
5. Rode o workflow.

O caminho esperado é:

1. `Validate CI secrets`
2. `Build web export`
3. `Build iOS IPA`
4. `Deploy iOS to TestFlight`

## Comando equivalente pelo terminal

```bash
cd app-front-main
yarn release:github:run --version-name 1.0.0 --release-target ios
```

## Validação local antes do release

```bash
cd app-front-main
yarn install --frozen-lockfile
yarn release:check-env
yarn lint
yarn test
yarn test:contracts:smoke
yarn build
npx cap sync ios
```

Para abrir no Xcode:

```bash
cd app-front-main
npx cap open ios
```

## Atenção sobre teste remoto

O comando abaixo força o app iOS local a abrir a versão web remota:

```bash
cd app-front-main
yarn ios:remote:signin:copy
npx cap open ios
```

Use isso somente para teste manual rápido no iPhone. Para App Store/TestFlight, não use `CAPACITOR_SERVER_URL`; o app deve ser empacotado com `webDir=out` e API de produção em `NEXT_PUBLIC_API_URL`.

## Aceite antes de enviar para revisão

- App abre em iPhone real via TestFlight.
- Login e criação de conta funcionam.
- Workspace, pacientes, internações e evolução funcionam.
- Na criação de evolução, aparece `Desfecho da internação` com:
  - `Manter internado (visita)`
  - `Alta hospitalar`
  - `Óbito`
- Alta e óbito removem a internação da lista de pendentes após refresh.
- Ditado por voz pede permissão corretamente.
- Nenhum build aponta para `localhost` ou IP local.
- App Privacy e política de privacidade batem com o comportamento real do app.
