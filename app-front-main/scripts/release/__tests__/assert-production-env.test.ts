import { describe, expect, it } from 'vitest'

import { validateProductionEnv } from '../assert-production-env.mjs'

const validEnv = {
  NEXT_PUBLIC_API_URL: 'https://api.link.strivium.com.br',
  NEXT_PUBLIC_TURNSTILE_SITE_KEY: '0x4AAAAA-production-key',
  NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION: 'false',
  NEXT_PUBLIC_EXPERIMENTAL_SBAR_AI_DICTATION: 'false',
}

describe('validateProductionEnv', () => {
  it('accepts the production store environment', () => {
    expect(validateProductionEnv(validEnv)).toEqual([])
  })

  it('rejects localhost API URLs and enabled experimental store flags', () => {
    expect(
      validateProductionEnv({
        ...validEnv,
        NEXT_PUBLIC_API_URL: 'http://localhost:55000',
        NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION: 'true',
        NEXT_PUBLIC_EXPERIMENTAL_SBAR_AI_DICTATION: 'true',
        CAPACITOR_LIVE_RELOAD: 'true',
      }),
    ).toEqual([
      'NEXT_PUBLIC_API_URL must use https:// for store builds.',
      'NEXT_PUBLIC_API_URL must not point to localhost or a private development host.',
      'CAPACITOR_LIVE_RELOAD must not be true for store builds.',
      'NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION must be false for the first store release.',
      'NEXT_PUBLIC_EXPERIMENTAL_SBAR_AI_DICTATION must be false for the first store release.',
    ])
  })

  it('rejects placeholder turnstile values for store builds', () => {
    expect(
      validateProductionEnv({
        ...validEnv,
        NEXT_PUBLIC_TURNSTILE_SITE_KEY: 'replace-with-production-turnstile-site-key',
      }),
    ).toEqual([
      'NEXT_PUBLIC_TURNSTILE_SITE_KEY must be a real production Turnstile site key (placeholder value detected).',
    ])
  })

  it('rejects Cloudflare test site keys for store builds', () => {
    expect(
      validateProductionEnv({
        ...validEnv,
        NEXT_PUBLIC_TURNSTILE_SITE_KEY: '1x00000000000000000000AA',
      }),
    ).toEqual(['NEXT_PUBLIC_TURNSTILE_SITE_KEY must not use Cloudflare test keys for store builds.'])
  })
})
