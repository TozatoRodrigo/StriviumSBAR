'use client'

import { SigninMutationProps, useSigninMutation } from '@/hooks/mutations/auth'
import { createContext, useContext, ReactNode, useMemo, useCallback } from 'react'
import { useAuthToken } from './AuthTokenContext'
import { useRouter } from 'next/navigation'
import { useWorkspaceToken } from './WorkspaceTokenContext'
import { useSnackbar } from 'notistack'
import { useUser } from '@/hooks/queries/user'
import { useQueryClient } from '@tanstack/react-query'

type AuthContextType = {
  login: (credentials: SigninMutationProps) => void
  logout: () => void
  info: ReturnType<typeof useUser>['data']
  states: { isAuthenticating: boolean; isAuth: boolean }
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType)

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const nav = useRouter()
  const { tokens, addTokens: addTokens, clear: clearAuthTokens } = useAuthToken()
  const { clear: clearWorkspaceTokens } = useWorkspaceToken()
  const { mutateAsync, isPending } = useSigninMutation()
  const { enqueueSnackbar } = useSnackbar()
  const queryClient = useQueryClient()

  // TODO: verificar se está expirado
  const isAuth = useMemo<boolean>(() => !!tokens?.access, [tokens?.access])
  const { data: authInfo } = useUser({ enabled: isAuth })

  const login = useCallback(
    (props: SigninMutationProps) => {
      mutateAsync(props)
        .then(({ access_token, refresh_token }) => addTokens({ access: access_token, refresh: refresh_token }))
        .then(() => nav.push('/'))
        .catch(() => enqueueSnackbar('Credenciais inválidas!'))
    },
    [addTokens, enqueueSnackbar, mutateAsync, nav]
  )

  const logout = useCallback(() => {
    clearWorkspaceTokens()
    clearAuthTokens()
    queryClient.clear()
  }, [clearAuthTokens, clearWorkspaceTokens, queryClient])

  const value = useMemo<AuthContextType>(
    () => ({
      login,
      logout,
      info: authInfo,
      states: {
        isAuth,
        isAuthenticating: isPending,
      },
    }),
    [authInfo, isAuth, isPending, login, logout]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => useContext(AuthContext)
