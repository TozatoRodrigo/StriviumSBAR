#!/usr/bin/env node

const PROFILE_REQUIREMENTS = {
  'build-web': ['NEXT_PUBLIC_TURNSTILE_SITE_KEY'],
  'android-build': [
    'ANDROID_KEYSTORE_BASE64',
    'ANDROID_KEYSTORE_PASSWORD',
    'ANDROID_KEY_ALIAS',
    'ANDROID_KEY_PASSWORD',
  ],
  'ios-build': [
    'MATCH_GIT_URL',
    'MATCH_PASSWORD',
    'APP_STORE_CONNECT_API_KEY_KEY_ID',
    'APP_STORE_CONNECT_API_KEY_ISSUER_ID',
    'APP_STORE_CONNECT_API_KEY_KEY',
  ],
  'android-deploy': ['GOOGLE_PLAY_CREDENTIALS'],
  'ios-deploy': [
    'APP_STORE_CONNECT_API_KEY_KEY_ID',
    'APP_STORE_CONNECT_API_KEY_ISSUER_ID',
    'APP_STORE_CONNECT_API_KEY_KEY',
  ],
}

const PROFILE_ALTERNATIVE_REQUIREMENTS = {
  'ios-build': [
    [
      'MATCH_GIT_PRIVATE_KEY',
      'MATCH_GIT_PRIVATE_KEY_BASE64',
      'MATCH_GIT_BASIC_AUTHORIZATION',
    ],
  ],
}

export function listKnownProfiles() {
  return Object.keys(PROFILE_REQUIREMENTS)
}

export function validateCiSecrets(profile, env = process.env) {
  if (!PROFILE_REQUIREMENTS[profile]) {
    throw new Error(
      `Unknown profile "${profile}". Expected one of: ${listKnownProfiles().join(', ')}`,
    )
  }

  const errors = []
  const requiredKeys = PROFILE_REQUIREMENTS[profile]

  for (const key of requiredKeys) {
    if (!env[key] || env[key].trim() === '') {
      errors.push(`${key} is required for profile "${profile}".`)
    }
  }

  const alternatives = PROFILE_ALTERNATIVE_REQUIREMENTS[profile] ?? []
  for (const alternativeGroup of alternatives) {
    const hasAtLeastOne = alternativeGroup.some(key => env[key] && env[key].trim() !== '')
    if (!hasAtLeastOne) {
      errors.push(
        `At least one of [${alternativeGroup.join(', ')}] is required for profile "${profile}".`,
      )
    }
  }

  return errors
}

export function assertCiSecrets(profile, env = process.env) {
  const errors = validateCiSecrets(profile, env)
  if (errors.length > 0) {
    throw new Error(`CI secret validation failed:\n- ${errors.join('\n- ')}`)
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const profile = process.argv[2]

  if (!profile) {
    console.error(`Usage: node scripts/release/assert-ci-secrets.mjs <${listKnownProfiles().join('|')}>`)
    process.exitCode = 1
  } else {
    try {
      assertCiSecrets(profile)
      console.log(`CI secret validation passed for profile "${profile}".`)
    } catch (error) {
      console.error(error.message)
      process.exitCode = 1
    }
  }
}
