#!/usr/bin/env node

import { execSync, spawnSync } from 'node:child_process'

function parseArgs(argv) {
  const args = {
    dryRun: false,
    repo: undefined,
    versionName: undefined,
    googlePlayTrack: 'internal',
  }

  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index]

    if (value === '--dry-run') {
      args.dryRun = true
    } else if (value === '--repo') {
      args.repo = argv[index + 1]
      index += 1
    } else if (value === '--version-name') {
      args.versionName = argv[index + 1]
      index += 1
    } else if (value === '--google-play-track') {
      args.googlePlayTrack = argv[index + 1]
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

function ensureGhIsAuthenticated() {
  const result = spawnSync('gh', ['auth', 'status'], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  })

  if (result.status !== 0) {
    throw new Error(
      'GitHub CLI is not authenticated. Run "gh auth login -w" and execute this command again.',
    )
  }
}

function runGhCommand(commandArgs) {
  const result = spawnSync('gh', commandArgs, {
    encoding: 'utf8',
    stdio: ['inherit', 'pipe', 'pipe'],
  })

  if (result.status !== 0) {
    throw new Error(result.stderr || result.stdout || 'Failed to run gh workflow command.')
  }
}

function printUsage() {
  console.log(
    'Usage: node scripts/release/run-mobile-release.mjs --version-name 1.0.0 [--google-play-track internal|alpha|beta|production] [--repo owner/name] [--dry-run]',
  )
}

export function runMobileRelease({
  versionName,
  googlePlayTrack = 'internal',
  repo = undefined,
  dryRun = false,
} = {}) {
  if (!versionName || versionName.trim() === '') {
    throw new Error('Missing --version-name.')
  }

  const validTracks = ['internal', 'alpha', 'beta', 'production']
  if (!validTracks.includes(googlePlayTrack)) {
    throw new Error(
      `Invalid --google-play-track "${googlePlayTrack}". Expected one of: ${validTracks.join(', ')}`,
    )
  }

  const repoFullName = repo || inferRepoFromGit()
  const ghArgs = [
    'workflow',
    'run',
    'mobile-release.yml',
    '--repo',
    repoFullName,
    '--field',
    `version_name=${versionName}`,
    '--field',
    `google_play_track=${googlePlayTrack}`,
  ]

  if (dryRun) {
    console.log(`[dry-run] gh ${ghArgs.join(' ')}`)
    return
  }

  ensureGhIsAuthenticated()
  runGhCommand(ghArgs)
  console.log(`Mobile Release workflow triggered for ${repoFullName} (version ${versionName}, track ${googlePlayTrack}).`)
}

if (import.meta.url === `file://${process.argv[1]}`) {
  try {
    const args = parseArgs(process.argv.slice(2))
    if (args.help) {
      printUsage()
      process.exit(0)
    }

    runMobileRelease({
      versionName: args.versionName,
      googlePlayTrack: args.googlePlayTrack,
      repo: args.repo,
      dryRun: args.dryRun,
    })
  } catch (error) {
    console.error(error.message)
    process.exitCode = 1
  }
}
