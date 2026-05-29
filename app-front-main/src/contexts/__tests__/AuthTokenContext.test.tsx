import { act, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { AUTH_LOCAL_STORAGE_KEY, AUTH_REFRESH_LOCAL_STORAGE_KEY } from '@/constants/auth'
import { AuthTokenProvider, useAuthToken } from '../AuthTokenContext'

const { refreshMutation } = vi.hoisted(() => ({
  refreshMutation: vi.fn(),
}))

vi.mock('@/hooks/mutations/auth', () => ({
  useUserRefreshToken: () => ({ mutateAsync: refreshMutation }),
}))

const encodeJwt = (payload: Record<string, unknown>) => {
  const header = { alg: 'none', typ: 'JWT' }
  const toBase64Url = (value: unknown) =>
    btoa(JSON.stringify(value)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '')
  return `${toBase64Url(header)}.${toBase64Url(payload)}.signature`
}

const Probe = () => {
  const { tokens } = useAuthToken()
  return <span data-testid="access-token">{tokens?.access ?? 'none'}</span>
}

describe('AuthTokenContext', () => {
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

  it('clears tokens when refresh fails for an expired access token', async () => {
    const nowSeconds = Math.floor(Date.now() / 1000)
    const expiredAccessToken = encodeJwt({ exp: nowSeconds - 60, sub: 'user-1', type: 'user' })
    const refreshToken = encodeJwt({ exp: nowSeconds + 3600, sub: 'user-1', type: 'user-refresh' })

    localStorage.setItem(AUTH_LOCAL_STORAGE_KEY, expiredAccessToken)
    localStorage.setItem(AUTH_REFRESH_LOCAL_STORAGE_KEY, refreshToken)
    refreshMutation.mockRejectedValueOnce(new Error('refresh failed'))

    render(
      <AuthTokenProvider>
        <Probe />
      </AuthTokenProvider>
    )

    await act(async () => {
      await vi.runOnlyPendingTimersAsync()
      await Promise.resolve()
    })

    expect(refreshMutation).toHaveBeenCalledWith({ refresh_token: refreshToken })
    expect(localStorage.getItem(AUTH_LOCAL_STORAGE_KEY)).toBeNull()
    expect(localStorage.getItem(AUTH_REFRESH_LOCAL_STORAGE_KEY)).toBeNull()
    expect(screen.getByTestId('access-token')).toHaveTextContent('none')
  })

  it('refreshes tokens automatically before expiration', async () => {
    const nowSeconds = Math.floor(Date.now() / 1000)
    const accessToken = encodeJwt({ exp: nowSeconds + 600, sub: 'user-1', type: 'user' })
    const refreshToken = encodeJwt({ exp: nowSeconds + 3600, sub: 'user-1', type: 'user-refresh' })
    const rotatedAccessToken = encodeJwt({ exp: nowSeconds + 7200, sub: 'user-1', type: 'user' })
    const rotatedRefreshToken = encodeJwt({
      exp: nowSeconds + 7200,
      sub: 'user-1',
      type: 'user-refresh',
    })

    localStorage.setItem(AUTH_LOCAL_STORAGE_KEY, accessToken)
    localStorage.setItem(AUTH_REFRESH_LOCAL_STORAGE_KEY, refreshToken)
    refreshMutation.mockResolvedValueOnce({
      access_token: rotatedAccessToken,
      refresh_token: rotatedRefreshToken,
    })

    render(
      <AuthTokenProvider>
        <Probe />
      </AuthTokenProvider>
    )

    await act(async () => {
      await vi.advanceTimersByTimeAsync(5 * 60 * 1000)
      await Promise.resolve()
    })

    expect(refreshMutation).toHaveBeenCalledWith({ refresh_token: refreshToken })
    expect(localStorage.getItem(AUTH_LOCAL_STORAGE_KEY)).toBe(rotatedAccessToken)
    expect(localStorage.getItem(AUTH_REFRESH_LOCAL_STORAGE_KEY)).toBe(rotatedRefreshToken)
  })
})
