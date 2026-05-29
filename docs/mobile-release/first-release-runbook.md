# Strivium Link First Release Runbook

This runbook moves the current repository from "ready" to the first internal mobile release.

## Step 1 - Configure GitHub variables and secrets

Reference: [github-secrets-setup.md](./github-secrets-setup.md)

Set these repository variables:

- `NEXT_PUBLIC_API_URL=https://strivium.link.servidortozato.cloud/api`
- `NEXT_PUBLIC_TURNSTILE_SITE_KEY=<production-turnstile-site-key>`

Set these repository secrets according to the first target:

For Android/Google Play:

- `ANDROID_KEYSTORE_BASE64` (base64 of upload/release keystore)
- `ANDROID_KEYSTORE_PASSWORD`
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`
- `GOOGLE_PLAY_CREDENTIALS` (full JSON service account key content)

For iOS/App Store:

- `MATCH_GIT_URL` (for example `git@github.com:org/certificates.git`)
- `MATCH_PASSWORD`
- `MATCH_GIT_PRIVATE_KEY` or `MATCH_GIT_PRIVATE_KEY_BASE64` or `MATCH_GIT_BASIC_AUTHORIZATION`
- `APP_STORE_CONNECT_API_KEY_KEY_ID`
- `APP_STORE_CONNECT_API_KEY_ISSUER_ID`
- `APP_STORE_CONNECT_API_KEY_KEY`

Notes:

- `APP_STORE_CONNECT_API_KEY_KEY` can be raw `.p8` key content or base64.
- `MATCH_GIT_PRIVATE_KEY` should contain the full private key text, including begin/end lines.

## Step 2 - Confirm Apple and Google app setup

- App IDs must match `br.com.strivium.link`.
- Apple app must exist in App Store Connect with bundle ID `br.com.strivium.link`.
- Google app must exist in Play Console with package `br.com.strivium.link`.
- Test groups must exist:
  - TestFlight internal group.
  - Play Console Internal Testing track.

## Step 3 - Validate backend production readiness

- Production API online over HTTPS.
- After the current backend code is deployed, health endpoint responds:
  - `GET https://strivium.link.servidortozato.cloud/api/health` -> `{"status":"ok"}`
- CORS allows:
  - `https://strivium.link.servidortozato.cloud`
  - `capacitor://localhost`

## Step 4 - Trigger first release workflow

Use `Actions > Mobile Release > Run workflow` with:

- `version_name`: `1.0.0` (or your target version)
- `release_target`: `ios`, `android`, or `all`
- `google_play_track`: `internal`

Optional CLI command:

```bash
cd app-front-main
yarn release:github:run --version-name 1.0.0 --release-target ios
```

Expected iOS-only flow:

1. `Validate CI secrets`
2. `Build web export`
3. `Build iOS IPA`
4. `Deploy iOS to TestFlight`

Expected full flow with `release_target=all`:

1. `Validate CI secrets`
2. `Build web export`
3. `Build Android AAB`
4. `Build iOS IPA`
5. `Deploy Android to Google Play`
6. `Deploy iOS to TestFlight`

If step 1 fails, fix secrets/vars and run again.

## Step 5 - Execute internal acceptance tests

Follow [release-checklist.md](./release-checklist.md) and validate in real devices:

- Login/logout
- Password recovery
- Workspace selection
- Patient and hospitalization flows
- Evolution flow

## Step 6 - Approve production rollout

After internal acceptance:

- Keep Android rollout gradual (`internal` -> `alpha/beta` -> `production`).
- Keep iOS on TestFlight until sign-off from product and clinical stakeholders.
