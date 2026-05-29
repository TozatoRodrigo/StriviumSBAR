# GitHub Secrets Setup for Mobile Release

Use this guide to prepare the exact values required by `.github/workflows/mobile-release.yml`.

## Variables

Create repository variables:

- `NEXT_PUBLIC_API_URL`: `https://strivium.link.servidortozato.cloud/api`
- `NEXT_PUBLIC_TURNSTILE_SITE_KEY`: production Cloudflare Turnstile site key

## Android secrets

Generate base64 for keystore:

```bash
base64 -i /absolute/path/to/strivium-release.keystore | tr -d '\n'
```

Store the resulting single line in:

- `ANDROID_KEYSTORE_BASE64`

Also set:

- `ANDROID_KEYSTORE_PASSWORD`
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`

## Google Play secret

Use the full JSON content from Google service account key in:

- `GOOGLE_PLAY_CREDENTIALS`

## iOS signing secrets

Set:

- `MATCH_GIT_URL`
- `MATCH_PASSWORD`

For match repo auth, use one:

- `MATCH_GIT_PRIVATE_KEY` (recommended), or
- `MATCH_GIT_PRIVATE_KEY_BASE64` (recommended for CLI automation), or
- `MATCH_GIT_BASIC_AUTHORIZATION`

Set App Store Connect API key values:

- `APP_STORE_CONNECT_API_KEY_KEY_ID`
- `APP_STORE_CONNECT_API_KEY_ISSUER_ID`
- `APP_STORE_CONNECT_API_KEY_KEY`

`APP_STORE_CONNECT_API_KEY_KEY` accepts:

- raw `.p8` text content, or
- base64 of `.p8` content

Base64 command:

```bash
base64 -i /absolute/path/to/AuthKey_XXXXXXXXXX.p8 | tr -d '\n'
```

## Quick verification

After adding variables/secrets, trigger `Mobile Release` manually and confirm the `Validate CI secrets` job passes first.

For App Store/TestFlight only, choose `release_target=ios`. In this mode Android keystore and Google Play secrets are not required.

For Google Play only, choose `release_target=android`. In this mode iOS signing secrets are not required.

## Optional bootstrap command

If all required values are exported in your shell, you can configure repo variables/secrets in one command:

```bash
cd app-front-main
yarn release:github:bootstrap
```

Dry run:

```bash
cd app-front-main
yarn release:github:bootstrap --dry-run
```

Suggested env file flow:

```bash
cd app-front-main
cp .env.github.release.example .env.github.release.local
```

Fill `.env.github.release.local`, then:

```bash
cd app-front-main
set -a
source .env.github.release.local
set +a
yarn release:github:bootstrap
```
