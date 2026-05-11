'use client'

import { AUTH_LOCAL_STORAGE_KEY, AUTH_REFRESH_LOCAL_STORAGE_KEY } from '@/constants/auth'
import { useUserRefreshToken } from '@/hooks/mutations/auth'
import { usePersistTokens } from '@/hooks/usePersistTokens'
import { decodeJwt } from '@/lib/utils'
import { differenceInMinutes } from 'date-fns'

import { createContext, useContext, ReactNode, useMemo, useEffect, useCallback, useRef } from 'react'

type AuthTokenContextType = ReturnType<typeof usePersistTokens> & {
  decoded: { access: AuthTokenPayload | null; refresh: unknown | null }
}

type AuthTokenPayload = {
  exp: number
  sub: string
  type: string
  user: {
    id: string
    first_name: string
    last_name: string
    email: string
  }
}

const AuthTokenContext = createContext<AuthTokenContextType>({} as AuthTokenContextType)

export const AuthTokenProvider = ({ children }: { children: ReactNode }) => {
  const { tokens, addTokens, clear } = usePersistTokens(AUTH_LOCAL_STORAGE_KEY, AUTH_REFRESH_LOCAL_STORAGE_KEY)
  const { mutateAsync: refreshTokenMutation } = useUserRefreshToken()
  const refreshTimeout = useRef<NodeJS.Timeout | null>(null)

  const decoded = useMemo(
    () => ({
      access: tokens?.access ? decodeJwt<AuthTokenPayload>(tokens.access) : null,
      refresh: tokens?.refresh ? decodeJwt(tokens.refresh) : null,
    }),
    [tokens?.access, tokens?.refresh]
  )

  const scheduleRefresh = useCallback(() => {
    if (!decoded.access?.exp || !tokens?.refresh) return

    const now = new Date()
    const exp = new Date(decoded.access.exp * 1000)
    const minutesUntilExpiry = differenceInMinutes(exp, now)
    const minutesBeforeRefresh = 5

    const msUntilRefresh = Math.max((minutesUntilExpiry - minutesBeforeRefresh) * 60 * 1000, 0)

    if (refreshTimeout.current) clearTimeout(refreshTimeout.current)

    refreshTimeout.current = setTimeout(async () => {
      try {
        const { access_token, refresh_token } = await refreshTokenMutation({
          refresh_token: tokens.refresh!,
        })
        addTokens({ access: access_token, refresh: refresh_token })
      } catch {
        clear()
      }
    }, msUntilRefresh)
  }, [decoded.access?.exp, tokens?.refresh, refreshTokenMutation, addTokens, clear])

  useEffect(() => {
    scheduleRefresh()
    return () => {
      if (refreshTimeout.current) clearTimeout(refreshTimeout.current)
    }
  }, [scheduleRefresh])

  return <AuthTokenContext.Provider value={{ tokens, decoded, addTokens, clear }}>{children}</AuthTokenContext.Provider>
}

export const useAuthToken = () => useContext(AuthTokenContext)
