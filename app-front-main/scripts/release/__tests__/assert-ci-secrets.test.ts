import { describe, expect, it } from 'vitest'

import { validateCiSecrets } from '../assert-ci-secrets.mjs'

const baseEnv = {
  NEXT_PUBLIC_TURNSTILE_SITE_KEY: '0x4AAAAA-production-key',
  ANDROID_KEYSTORE_BASE64: 'ZmFrZS1rZXlzdG9yZQ==',
  ANDROID_KEYSTORE_PASSWORD: 'keystore-password',
  ANDROID_KEY_ALIAS: 'strivium-upload',
  ANDROID_KEY_PASSWORD: 'alias-password',
  GOOGLE_PLAY_CREDENTIALS: '{"type":"service_account"}',
  MATCH_GIT_URL: 'git@github.com:strivium/certificates.git',
  MATCH_PASSWORD: 'match-password',
  MATCH_GIT_PRIVATE_KEY: '-----BEGIN PRIVATE KEY-----\nabc\n-----END PRIVATE KEY-----',
  APP_STORE_CONNECT_API_KEY_KEY_ID: 'ABC1234567',
  APP_STORE_CONNECT_API_KEY_ISSUER_ID: '11111111-2222-3333-4444-555555555555',
  APP_STORE_CONNECT_API_KEY_KEY: 'LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0t',
}

describe('validateCiSecrets', () => {
  it('accepts a fully configured ios-build profile', () => {
    expect(validateCiSecrets('ios-build', baseEnv)).toEqual([])
  })

  it('requires one authentication option for match git storage', () => {
    expect(
      validateCiSecrets('ios-build', {
        ...baseEnv,
        MATCH_GIT_PRIVATE_KEY: '',
      }),
    ).toEqual([
      'At least one of [MATCH_GIT_PRIVATE_KEY, MATCH_GIT_PRIVATE_KEY_BASE64, MATCH_GIT_BASIC_AUTHORIZATION] is required for profile "ios-build".',
    ])
  })

  it('reports missing Android secrets for android-build', () => {
    expect(
      validateCiSecrets('android-build', {
        ...baseEnv,
        ANDROID_KEYSTORE_PASSWORD: '',
        ANDROID_KEY_PASSWORD: '',
      }),
    ).toEqual([
      'ANDROID_KEYSTORE_PASSWORD is required for profile "android-build".',
      'ANDROID_KEY_PASSWORD is required for profile "android-build".',
    ])
  })
})
