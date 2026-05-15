import fs from 'node:fs'
import path from 'node:path'
import { describe, expect, it } from 'vitest'

const root = process.cwd()

function read(relativePath: string) {
  return fs.readFileSync(path.join(root, relativePath), 'utf8')
}

describe('API contract smoke', () => {
  it('uses tenant refresh endpoint under auth module', () => {
    const content = read('src/hooks/mutations/workspaces.ts')
    expect(content).toContain("/auth/v1/refresh/tenant")
    expect(content).not.toContain("/tenant/v1/refresh/tenant")
  })

  it('uses doctor CRUD endpoints', () => {
    const mutationsContent = read('src/hooks/mutations/doctors.ts')
    const queriesContent = read('src/hooks/queries/doctors.ts')

    expect(mutationsContent).toContain("/doctor/v1/doctors")
    expect(mutationsContent).toContain("`/doctor/v1/doctors/${id}`")
    expect(queriesContent).toContain("/doctor/v1/doctors")
    expect(queriesContent).toContain("`/doctor/v1/doctors/${id}`")
  })

  it('resolves SBAR endpoint without duplicating /api in production', () => {
    const content = read('src/hooks/mutations/sbar.ts')

    expect(content).toContain("endsWith('/api')")
    expect(content).toContain("'/sbar/extract'")
    expect(content).toContain("'/api/sbar/extract'")
  })
})
