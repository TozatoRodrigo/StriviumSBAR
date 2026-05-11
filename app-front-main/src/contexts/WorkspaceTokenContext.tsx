'use client'

import { createContext, useContext, ReactNode, useMemo, useCallback, useRef, useEffect } from 'react'
import { WORKSPACE_LOCAL_STORAGE_KEY, WORKSPACE_REFRESH_LOCAL_STORAGE_KEY } from '@/constants/workspace'
import { usePersistTokens } from '@/hooks/usePersistTokens'
import { decodeJwt } from '@/lib/utils'
import { differenceInMinutes } from 'date-fns'
import { useWorkspaceRefreshToken } from '@/hooks/mutations/workspaces'

type WorkspaceTokenContextType = ReturnType<typeof usePersistTokens> & {
  decoded: { access: WorkspaceTokenPayload | null; refresh: unknown | null }
}

type WorkspaceTokenPayload = {
  exp: number
  sub: string
  type: string
  tenant: {
    id: string
    name: string
  }
  user: {
    id: string
    first_name: string
    last_name: string
    email: string
  }
  role: {
    id: string
    name: string
    permissions: { code: string; name: string }[]
  }
}

const WorkspaceTokenContext = createContext<WorkspaceTokenContextType>({} as WorkspaceTokenContextType)

export const WorkspaceTokenProvider = ({ children }: { children: ReactNode }) => {
  const { tokens, addTokens, clear } = usePersistTokens(
    WORKSPACE_LOCAL_STORAGE_KEY,
    WORKSPACE_REFRESH_LOCAL_STORAGE_KEY
  )
  const { mutateAsync: refreshTokenMutation } = useWorkspaceRefreshToken()
  const refreshTimeout = useRef<NodeJS.Timeout | null>(null)

  const decoded = useMemo(
    () => ({
      access: tokens?.access ? decodeJwt<WorkspaceTokenPayload>(tokens.access) : null,
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

  return (
    <WorkspaceTokenContext.Provider value={{ tokens, decoded, addTokens, clear }}>
      {children}
    </WorkspaceTokenContext.Provider>
  )
}

export const useWorkspaceToken = () => useContext(WorkspaceTokenContext)
