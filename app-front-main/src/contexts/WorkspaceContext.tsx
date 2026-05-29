'use client'

import { createContext, useContext, ReactNode, useMemo, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { useWorkspaceToken } from './WorkspaceTokenContext'
import { useSnackbar } from 'notistack'
import { useSigninWorkspaceMutation } from '@/hooks/mutations/workspaces'

type WorkspaceContextType = {
  select: (id: string) => void
  exit: () => void
  info: ReturnType<typeof useWorkspaceToken>['decoded']['access']
  states: { isAuthenticating: boolean; isAuth: boolean; isRole: { admin: boolean } }
}

const WorkspaceContext = createContext<WorkspaceContextType>({} as WorkspaceContextType)

export const WorkspaceProvider = ({ children }: { children: ReactNode }) => {
  const nav = useRouter()
  const { tokens, decoded, addTokens: addTokens, clear: clearWorkspaceTokens } = useWorkspaceToken()

  const { mutateAsync, isPending } = useSigninWorkspaceMutation()
  const { enqueueSnackbar } = useSnackbar()

  const isAuth = useMemo<boolean>(() => {
    if (!tokens?.access || !decoded.access?.exp) return false
    return decoded.access.exp * 1000 > Date.now()
  }, [decoded.access?.exp, tokens?.access])

  const select = useCallback(
    (tenant_id: string) => {
      mutateAsync({ tenant_id })
        .then(({ access_token, refresh_token }) => addTokens({ access: access_token, refresh: refresh_token }))
        .then(() => nav.push('/'))
        .catch(() => enqueueSnackbar('Local de trabalho inválido!'))
    },
    [addTokens, enqueueSnackbar, mutateAsync, nav]
  )
  const isWorkspaceAdmin = useMemo(() => decoded.access?.role.name === 'admin', [decoded.access?.role.name])

  const exit = useCallback(() => {
    clearWorkspaceTokens()
  }, [clearWorkspaceTokens])

  const value = useMemo<WorkspaceContextType>(
    () => ({
      select,
      exit,
      info: decoded.access,
      states: {
        isAuth,
        isAuthenticating: isPending,
        isRole: {
          admin: isWorkspaceAdmin,
        },
      },
    }),
    [select, exit, decoded.access, isAuth, isPending, isWorkspaceAdmin]
  )

  return <WorkspaceContext.Provider value={value}>{children}</WorkspaceContext.Provider>
}

export const useWorkspace = () => useContext(WorkspaceContext)
