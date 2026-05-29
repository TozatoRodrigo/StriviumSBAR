# Strivium Link Mobile Release Checklist

Use this checklist for every App Store/TestFlight and Google Play release.

For the first release setup, follow [first-release-runbook.md](./first-release-runbook.md) before this checklist.

## Accounts and Access

- [ ] Apple Developer Program active.
- [ ] App Store Connect app created for `br.com.strivium.link`.
- [ ] Google Play Console app created for `br.com.strivium.link`.
- [ ] GitHub environment `production` has required reviewers.
- [ ] App review demo account exists with fictitious clinical data.
- [ ] Support URL and privacy policy URL are public, active, and not geofenced.

## Production Environment

- [ ] `NEXT_PUBLIC_API_URL=https://strivium.link.servidortozato.cloud/api`.
- [ ] `NEXT_PUBLIC_TURNSTILE_SITE_KEY` is a production Cloudflare Turnstile site key.
- [ ] `NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION=false`.
- [ ] `NEXT_PUBLIC_EXPERIMENTAL_SBAR_AI_DICTATION=false`.
- [ ] `CAPACITOR_LIVE_RELOAD` is unset or `false`.
- [ ] Backend runs over HTTPS and `GET https://strivium.link.servidortozato.cloud/api/health` returns `{"status":"ok"}` after the current backend code is deployed.
- [ ] Backend CORS includes `https://strivium.link.servidortozato.cloud` and `capacitor://localhost`.
- [ ] Backend `ENABLE_DOCS=false`, `FILESYSTEM_DRIVER=s3`, SMTP configured, and backups enabled.

## GitHub Secrets and Variables

- [ ] Variable `NEXT_PUBLIC_API_URL`.
- [ ] Variable `NEXT_PUBLIC_TURNSTILE_SITE_KEY`.
- [ ] For iOS: `MATCH_GIT_URL`.
- [ ] For iOS: `MATCH_PASSWORD`.
- [ ] For iOS: `MATCH_GIT_PRIVATE_KEY` or `MATCH_GIT_PRIVATE_KEY_BASE64` or `MATCH_GIT_BASIC_AUTHORIZATION`.
- [ ] For iOS: `APP_STORE_CONNECT_API_KEY_KEY_ID`.
- [ ] For iOS: `APP_STORE_CONNECT_API_KEY_ISSUER_ID`.
- [ ] For iOS: `APP_STORE_CONNECT_API_KEY_KEY`.
- [ ] For Android: `ANDROID_KEYSTORE_BASE64`.
- [ ] For Android: `ANDROID_KEYSTORE_PASSWORD`.
- [ ] For Android: `ANDROID_KEY_ALIAS`.
- [ ] For Android: `ANDROID_KEY_PASSWORD`.
- [ ] For Android: `GOOGLE_PLAY_CREDENTIALS`.

## Build Gates

- [ ] `cd app-front-main && yarn release:check-env`.
- [ ] `cd app-front-main && yarn lint`.
- [ ] `cd app-front-main && yarn test`.
- [ ] `cd app-front-main && yarn test:contracts:smoke`.
- [ ] `cd app-front-main && yarn build`.
- [ ] `cd app-api-main && APP_ENV=testing poetry run pytest`.
- [ ] `cd app-api-main && poetry run ruff check app`.
- [ ] `cd app-api-main && poetry run ruff format --check app`.

## Store Submission

- [ ] Android AAB uploaded to Internal Testing first.
- [ ] iOS IPA uploaded to TestFlight first.
- [ ] App opens on a real Android device and real iPhone.
- [ ] Reviewer can sign in with demo account.
- [ ] Store privacy forms match the behavior described in `privacy-data-map.md`.
- [ ] Screenshots show real app screens with fictitious data only.
- [ ] Release notes mention visible changes and any limitations relevant to review.
