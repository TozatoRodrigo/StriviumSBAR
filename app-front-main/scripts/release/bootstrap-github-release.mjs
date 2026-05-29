#!/usr/bin/env node

import { execSync, spawnSync } from 'node:child_process'

import { validateProductionEnv } from './assert-production-env.mjs'

const REQUIRED_VARIABLES = ['NEXT_PUBLIC_API_URL', 'NEXT_PUBLIC_TURNSTILE_SITE_KEY']

const REQUIRED_SECRETS = [
  'ANDROID_KEYSTORE_BASE64',
  'ANDROID_KEYSTORE_PASSWORD',
  'ANDROID_KEY_ALIAS',
  'ANDROID_KEY_PASSWORD',
  'GOOGLE_PLAY_CREDENTIALS',
  'MATCH_GIT_URL',
  'MATCH_PASSWORD',
  'APP_STORE_CONNECT_API_KEY_KEY_ID',
  'APP_STORE_CONNECT_API_KEY_ISSUER_ID',
  'APP_STORE_CONNECT_API_KEY_KEY',
]

const SECRET_ALTERNATIVES = [
  ['MATCH_GIT_PRIVATE_KEY', 'MATCH_GIT_PRIVATE_KEY_BASE64', 'MATCH_GIT_BASIC_AUTHORIZATION'],
]

function parseArgs(argv) {
  const args = { dryRun: false, repo: undefined }

  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index]
    if (value === '--dry-run') {
      args.dryRun = true
    } else if (value === '--repo') {
      args.repo = argv[index + 1]
      index += 1
    } else if (value === '--help' || value === '-h') {
      args.help = true
    } else {
      throw new Error(`Unknown argument: ${value}`)
    }
  }

  return args
}

function parseRepoFromOrigin(originUrl) {
  const cleanedUrl = originUrl.trim()

  const sshMatch = cleanedUrl.match(/^git@github\.com:([^/]+\/[^/.]+)(?:\.git)?$/)
  if (sshMatch) {
    return sshMatch[1]
  }

  const httpsMatch = cleanedUrl.match(
    /^https:\/\/github\.com\/([^/]+\/[^/.]+)(?:\.git)?$/,
  )
  if (httpsMatch) {
    return httpsMatch[1]
  }

  throw new Error(
    `Could not infer repository from origin URL "${cleanedUrl}". Use --repo owner/name.`,
  )
}

function inferRepoFromGit() {
  const originUrl = execSync('git remote get-url origin', {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  }).trim()

  return parseRepoFromOrigin(originUrl)
}

function validateInputs(env) {
  const errors = [...validateProductionEnv(env)]

  for (const variableKey of REQUIRED_VARIABLES) {
    if (!env[variableKey] || env[variableKey].trim() === '') {
      errors.push(`${variableKey} is required to configure GitHub repository variables.`)
    }
  }

  for (const secretKey of REQUIRED_SECRETS) {
    if (!env[secretKey] || env[secretKey].trim() === '') {
      errors.push(`${secretKey} is required to configure GitHub repository secrets.`)
    }
  }

  for (const alternatives of SECRET_ALTERNATIVES) {
    const hasAny = alternatives.some(key => env[key] && env[key].trim() !== '')
    if (!hasAny) {
      errors.push(`At least one secret is required: ${alternatives.join(' or ')}.`)
    }
  }

  return errors
}

function runGhCommand(args, { input } = {}) {
  const result = spawnSync('gh', args, {
    input,
    encoding: 'utf8',
    stdio: ['pipe', 'pipe', 'pipe'],
  })

  if (result.status !== 0) {
    throw new Error(
      `Failed command: gh ${args.join(' ')}\n${result.stderr || result.stdout || 'Unknown gh error.'}`,
    )
  }
}

function ensureGhIsAuthenticated() {
  const result = spawnSync('gh', ['auth', 'status'], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  })

  if (result.status !== 0) {
    throw new Error(
      'GitHub CLI is not authenticated. Run "gh auth login -w" and execute this script again.',
    )
  }
}

function setVariable(repo, key, value, dryRun) {
  if (dryRun) {
    console.log(`[dry-run] gh variable set ${key} --repo ${repo} --body ***`)
    return
  }

  runGhCommand(['variable', 'set', key, '--repo', repo, '--body', value])
}

function setSecret(repo, key, value, dryRun) {
  if (dryRun) {
    console.log(`[dry-run] gh secret set ${key} --repo ${repo} --body ***`)
    return
  }

  runGhCommand(['secret', 'set', key, '--repo', repo], { input: value })
}

function printUsage() {
  console.log(
    'Usage: node scripts/release/bootstrap-github-release.mjs [--repo owner/name] [--dry-run]',
  )
}

export function bootstrapGithubRelease({
  env = process.env,
  repo = undefined,
  dryRun = false,
} = {}) {
  const repoFullName = repo || inferRepoFromGit()
  const errors = validateInputs(env)

  if (errors.length > 0) {
    throw new Error(`Bootstrap failed due to missing/invalid configuration:\n- ${errors.join('\n- ')}`)
  }

  if (!dryRun) {
    ensureGhIsAuthenticated()
  }

  console.log(`Configuring GitHub Actions variables and secrets for ${repoFullName}...`)

  for (const variableKey of REQUIRED_VARIABLES) {
    setVariable(repoFullName, variableKey, env[variableKey], dryRun)
  }

  for (const secretKey of REQUIRED_SECRETS) {
    setSecret(repoFullName, secretKey, env[secretKey], dryRun)
  }

  const matchPrivateKey = env.MATCH_GIT_PRIVATE_KEY?.trim()
  const matchPrivateKeyBase64 = env.MATCH_GIT_PRIVATE_KEY_BASE64?.trim()
  const matchBasicAuth = env.MATCH_GIT_BASIC_AUTHORIZATION?.trim()
  if (matchPrivateKey) {
    setSecret(repoFullName, 'MATCH_GIT_PRIVATE_KEY', matchPrivateKey, dryRun)
  } else if (matchPrivateKeyBase64) {
    const decodedMatchPrivateKey = Buffer.from(matchPrivateKeyBase64, 'base64').toString('utf8')
    if (!decodedMatchPrivateKey.includes('BEGIN') || !decodedMatchPrivateKey.includes('PRIVATE KEY')) {
      throw new Error('MATCH_GIT_PRIVATE_KEY_BASE64 did not decode to a valid private key.')
    }

    setSecret(repoFullName, 'MATCH_GIT_PRIVATE_KEY', decodedMatchPrivateKey, dryRun)
  } else if (matchBasicAuth) {
    setSecret(
      repoFullName,
      'MATCH_GIT_BASIC_AUTHORIZATION',
      matchBasicAuth,
      dryRun,
    )
  }

  console.log('GitHub release bootstrap completed.')
}

if (import.meta.url === `file://${process.argv[1]}`) {
  try {
    const args = parseArgs(process.argv.slice(2))
    if (args.help) {
      printUsage()
      process.exit(0)
    }

    bootstrapGithubRelease({
      repo: args.repo,
      dryRun: args.dryRun,
    })
  } catch (error) {
    console.error(error.message)
    process.exitCode = 1
  }
}
