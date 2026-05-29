import { act, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { WORKSPACE_LOCAL_STORAGE_KEY, WORKSPACE_REFRESH_LOCAL_STORAGE_KEY } from '@/constants/workspace'
import { WorkspaceTokenProvider, useWorkspaceToken } from '../WorkspaceTokenContext'

const { refreshMutation } = vi.hoisted(() => ({
  refreshMutation: vi.fn(),
}))

vi.mock('@/hooks/mutations/workspaces', () => ({
  useWorkspaceRefreshToken: () => ({ mutateAsync: refreshMutation }),
}))

const encodeJwt = (payload: Record<string, unknown>) => {
  const header = { alg: 'none', typ: 'JWT' }
  const toBase64Url = (value: unknown) =>
    btoa(JSON.stringify(value)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '')
  return `${toBase64Url(header)}.${toBase64Url(payload)}.signature`
}

const Probe = () => {
  const { tokens } = useWorkspaceToken()
  return <span data-testid="workspace-access-token">{tokens?.access ?? 'none'}</span>
}

describe('WorkspaceTokenContext', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2026-05-13T10:00:00.000Z'))
    localStorage.clear()
    refreshMutation.mockReset()
  })

  afterEach(() => {
    vi.useRealTimers()
    localStorage.clear()
  })

  it('clears workspace tokens when refresh fails for an expired access token', async () => {
    const nowSeconds = Math.floor(Date.now() / 1000)
    const expiredAccessToken = encodeJwt({
      exp: nowSeconds - 60,
      sub: 'tenant-1',
      type: 'tenant',
      role: { name: 'admin', permissions: [] },
    })
    const refreshToken = encodeJwt({
      exp: nowSeconds + 3600,
      sub: 'tenant-1',
      type: 'tenant-refresh',
      user_id: 'user-1',
    })

    localStorage.setItem(WORKSPACE_LOCAL_STORAGE_KEY, expiredAccessToken)
    localStorage.setItem(WORKSPACE_REFRESH_LOCAL_STORAGE_KEY, refreshToken)
    refreshMutation.mockRejectedValueOnce(new Error('refresh failed'))

    render(
      <WorkspaceTokenProvider>
        <Probe />
      </WorkspaceTokenProvider>
    )

    await act(async () => {
      await vi.runOnlyPendingTimersAsync()
      await Promise.resolve()
    })

    expect(refreshMutation).toHaveBeenCalledWith({ refresh_token: refreshToken })
    expect(localStorage.getItem(WORKSPACE_LOCAL_STORAGE_KEY)).toBeNull()
    expect(localStorage.getItem(WORKSPACE_REFRESH_LOCAL_STORAGE_KEY)).toBeNull()
    expect(screen.getByTestId('workspace-access-token')).toHaveTextContent('none')
  })

  it('refreshes workspace tokens automatically before expiration', async () => {
    const nowSeconds = Math.floor(Date.now() / 1000)
    const accessToken = encodeJwt({
      exp: nowSeconds + 600,
      sub: 'tenant-1',
      type: 'tenant',
      role: { name: 'admin', permissions: [] },
    })
    const refreshToken = encodeJwt({
      exp: nowSeconds + 3600,
      sub: 'tenant-1',
      type: 'tenant-refresh',
      user_id: 'user-1',
    })
    const rotatedAccessToken = encodeJwt({
      exp: nowSeconds + 7200,
      sub: 'tenant-1',
      type: 'tenant',
      role: { name: 'admin', permissions: [] },
    })
    const rotatedRefreshToken = encodeJwt({
      exp: nowSeconds + 7200,
      sub: 'tenant-1',
      type: 'tenant-refresh',
      user_id: 'user-1',
    })

    localStorage.setItem(WORKSPACE_LOCAL_STORAGE_KEY, accessToken)
    localStorage.setItem(WORKSPACE_REFRESH_LOCAL_STORAGE_KEY, refreshToken)
    refreshMutation.mockResolvedValueOnce({
      access_token: rotatedAccessToken,
      refresh_token: rotatedRefreshToken,
    })

    render(
      <WorkspaceTokenProvider>
        <Probe />
      </WorkspaceTokenProvider>
    )

    await act(async () => {
      await vi.advanceTimersByTimeAsync(5 * 60 * 1000)
      await Promise.resolve()
    })

    expect(refreshMutation).toHaveBeenCalledWith({ refresh_token: refreshToken })
    expect(localStorage.getItem(WORKSPACE_LOCAL_STORAGE_KEY)).toBe(rotatedAccessToken)
    expect(localStorage.getItem(WORKSPACE_REFRESH_LOCAL_STORAGE_KEY)).toBe(rotatedRefreshToken)
  })
})
