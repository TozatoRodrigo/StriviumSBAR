#!/usr/bin/env node

import { spawnSync } from 'node:child_process'

import { assertProductionEnv } from './assert-production-env.mjs'

const allowedPlatforms = new Set(['android', 'ios'])
const platform = process.argv[2]

assertProductionEnv()

if (platform && !allowedPlatforms.has(platform)) {
  console.error('Usage: node scripts/release/sync-native.mjs [android|ios]')
  process.exitCode = 1
} else {
  const npxCommand = process.platform === 'win32' ? 'npx.cmd' : 'npx'
  const args = ['cap', 'sync']
  if (platform) {
    args.push(platform)
  }
  const result = spawnSync(npxCommand, args, { stdio: 'inherit' })
  process.exitCode = result.status ?? 1
}
