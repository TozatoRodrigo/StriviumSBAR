#!/usr/bin/env node

const REQUIRED_ENV_KEYS = ['NEXT_PUBLIC_API_URL', 'NEXT_PUBLIC_TURNSTILE_SITE_KEY']
const INVALID_TURNSTILE_SITE_KEY_FRAGMENTS = ['replace-with-', 'placeholder']
const CLOUDFLARE_TURNSTILE_TEST_SITE_KEYS = new Set([
  '1x00000000000000000000AA',
  '2x00000000000000000000AB',
  '1x00000000000000000000BB',
  '2x00000000000000000000BB',
  '3x00000000000000000000FF',
])

const PRIVATE_HOST_PATTERNS = [
  /^localhost$/i,
  /^127\./,
  /^0\.0\.0\.0$/,
  /^10\./,
  /^192\.168\./,
  /^172\.(1[6-9]|2\d|3[0-1])\./,
  /^::1$/,
  /^.*\.local$/i,
]

export function validateProductionEnv(env = process.env) {
  const errors = []

  for (const key of REQUIRED_ENV_KEYS) {
    if (!env[key]) {
      errors.push(`${key} is required for store builds.`)
    }
  }

  if (env.NEXT_PUBLIC_API_URL) {
    try {
      const apiUrl = new URL(env.NEXT_PUBLIC_API_URL)
      if (apiUrl.protocol !== 'https:') {
        errors.push('NEXT_PUBLIC_API_URL must use https:// for store builds.')
      }
      if (PRIVATE_HOST_PATTERNS.some(pattern => pattern.test(apiUrl.hostname))) {
        errors.push('NEXT_PUBLIC_API_URL must not point to localhost or a private development host.')
      }
    } catch {
      errors.push('NEXT_PUBLIC_API_URL must be a valid absolute URL.')
    }
  }

  if (env.CAPACITOR_LIVE_RELOAD === 'true') {
    errors.push('CAPACITOR_LIVE_RELOAD must not be true for store builds.')
  }

  if (env.NEXT_PUBLIC_TURNSTILE_SITE_KEY) {
    const siteKey = env.NEXT_PUBLIC_TURNSTILE_SITE_KEY.trim()
    if (INVALID_TURNSTILE_SITE_KEY_FRAGMENTS.some(fragment => siteKey.includes(fragment))) {
      errors.push(
        'NEXT_PUBLIC_TURNSTILE_SITE_KEY must be a real production Turnstile site key (placeholder value detected).',
      )
    }
    if (CLOUDFLARE_TURNSTILE_TEST_SITE_KEYS.has(siteKey)) {
      errors.push('NEXT_PUBLIC_TURNSTILE_SITE_KEY must not use Cloudflare test keys for store builds.')
    }
  }

  if (env.NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION === 'true') {
    errors.push('NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION must be false for the first store release.')
  }

  if (env.NEXT_PUBLIC_EXPERIMENTAL_SBAR_AI_DICTATION === 'true') {
    errors.push('NEXT_PUBLIC_EXPERIMENTAL_SBAR_AI_DICTATION must be false for the first store release.')
  }

  return errors
}

export function assertProductionEnv(env = process.env) {
  const errors = validateProductionEnv(env)
  if (errors.length > 0) {
    throw new Error(`Store release environment is invalid:\n- ${errors.join('\n- ')}`)
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  try {
    assertProductionEnv()
    console.log('Store release environment is valid.')
  } catch (error) {
    console.error(error.message)
    process.exitCode = 1
  }
}
