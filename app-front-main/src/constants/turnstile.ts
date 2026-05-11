export const TURNSTILE_CONSTANTS = {
  DEFAULT_THEME: 'auto' as const,
  DEFAULT_SIZE: 'flexible' as const,
  DEFAULT_APPEARANCE: 'always' as const,
  DEFAULT_EXECUTION: 'render' as const,
  DEFAULT_RETRY: 'auto' as const,
  DEFAULT_RETRY_INTERVAL: 8000,
  DEFAULT_REFRESH_EXPIRED: 'auto' as const,
  DEFAULT_REFRESH_TIMEOUT: 'auto' as const,
  DEFAULT_RESPONSE_FIELD: true,
  DEFAULT_RESPONSE_FIELD_NAME: 'cf-turnstile-response',
  DEFAULT_FEEDBACK_ENABLED: true,
  DEFAULT_ID: 'turnstile-widget',

  SANDBOX_KEYS: {
    PASS: '1x00000000000000000000AA',
    BLOCK: '2x00000000000000000000AB',
    PASS_INVISIBLE: '1x00000000000000000000BB',
    BLOCK_INVISIBLE: '2x00000000000000000000BB',
  },

  SERVER_SANDBOX_KEYS: {
    PASS: '1x0000000000000000000000000000000AA',
    FAIL: '2x0000000000000000000000000000000AA',
    ERROR: '3x0000000000000000000000000000000AA',
  },

  API_ENDPOINT: 'https://challenges.cloudflare.com/turnstile/v0/siteverify',
  SCRIPT_URL: 'https://challenges.cloudflare.com/turnstile/v0/api.js',
} as const

export const TURNSTILE_ERROR_CODES = {
  MISSING_INPUT_SECRET: 'missing-input-secret',
  INVALID_INPUT_SECRET: 'invalid-input-secret',
  MISSING_INPUT_RESPONSE: 'missing-input-response',
  INVALID_INPUT_RESPONSE: 'invalid-input-response',
  BAD_REQUEST: 'bad-request',
  TIMEOUT_OR_DUPLICATE: 'timeout-or-duplicate',
  INTERNAL_ERROR: 'internal-error',
} as const
