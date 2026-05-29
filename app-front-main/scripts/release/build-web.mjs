#!/usr/bin/env node

import { spawnSync } from 'node:child_process'

import { assertProductionEnv } from './assert-production-env.mjs'

assertProductionEnv()

const yarnCommand = process.platform === 'win32' ? 'yarn.cmd' : 'yarn'
const result = spawnSync(yarnCommand, ['build'], {
  env: {
    ...process.env,
    NODE_ENV: 'production',
  },
  stdio: 'inherit',
})

process.exitCode = result.status ?? 1
