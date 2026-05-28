# Mobile Store Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepare Strivium Link for Apple App Store and Google Play release from the existing Capacitor app in `app-front-main`.

**Architecture:** Keep the current Next.js static export wrapped by Capacitor for iOS and Android. Use `app-api-main` as the production API, with a public health endpoint and root-level CI/CD workflows for repo-wide automation.

**Tech Stack:** Next.js, React, Capacitor 8, Fastlane, Android Gradle Plugin, Xcode, FastAPI, Poetry, GitHub Actions.

---

## Tasks

- [x] Add unauthenticated backend `GET /health` with a feature test.
- [x] Make Capacitor production-safe by disabling local `server.url` unless `CAPACITOR_LIVE_RELOAD=true`.
- [x] Add release scripts that validate store environment, build the web export, and sync native projects.
- [x] Upgrade Capacitor packages to v8 and align Android/iOS native minimums.
- [x] Generate Android AAB and iOS IPA through Fastlane lanes.
- [x] Move CI/CD workflows to `.github/workflows` at repository root.
- [x] Add store release docs for privacy, metadata, screenshots, and acceptance checks.

## Verification Commands

```bash
cd app-front-main
yarn release:check-env
yarn lint
yarn test
yarn test:contracts:smoke
yarn build
npx cap sync android
npx cap sync ios
```

```bash
cd app-api-main
APP_ENV=testing poetry run pytest
poetry run ruff check app
poetry run ruff format --check app
```

## Release Defaults

- Public app name: Strivium Link.
- Bundle ID and package name: `br.com.strivium.link`.
- Production web URL: `https://link.strivium.com.br`.
- Production API URL: `https://api.link.strivium.com.br`.
- First mobile store release keeps SBAR voice dictation and AI dictation flags disabled.
