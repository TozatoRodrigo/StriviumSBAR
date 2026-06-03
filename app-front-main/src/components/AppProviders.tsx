'use client'

import '@/lib/i18n'
import { Loader } from '@/components/Loader'
import { AuthProvider } from '@/contexts/AuthContext'
import { AuthTokenProvider } from '@/contexts/AuthTokenContext'
import { WorkspaceProvider } from '@/contexts/WorkspaceContext'
import { WorkspaceTokenProvider } from '@/contexts/WorkspaceTokenContext'
import { PwaInstallProvider } from '@/components/PwaInstallProvider'
import { AppRouterCacheProvider } from '@mui/material-nextjs/v15-appRouter'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { SnackbarProvider } from 'notistack'
import { Suspense, useEffect, useState } from 'react'
import { ThemeProvider } from '@mui/material/styles'
import dynamic from 'next/dynamic'

import { theme } from '@/theme'

const ReactQueryDevtools =
  process.env.NODE_ENV === 'development' && process.env.NEXT_PUBLIC_ENABLE_REACT_QUERY_DEVTOOLS === 'true'
    ? dynamic(
        () => import('@tanstack/react-query-devtools').then(mod => mod.ReactQueryDevtools),
        { ssr: false }
      )
    : null

type AppProvidersProps = Readonly<{
  children: React.ReactNode
}>

export function AppProviders({ children }: AppProvidersProps) {
  const [queryClient] = useState(() => new QueryClient())

  useEffect(() => {
    if (!('serviceWorker' in navigator)) return

    void navigator.serviceWorker.register('/sw.js').catch(() => undefined)
  }, [])

  return (
    <ThemeProvider theme={theme}>
      <SnackbarProvider anchorOrigin={{ horizontal: 'center', vertical: 'bottom' }}>
        <PwaInstallProvider>
          <Suspense fallback={<Loader />}>
            <QueryClientProvider client={queryClient}>
              <AppRouterCacheProvider options={{ enableCssLayer: true }}>
                <AuthTokenProvider>
                  <WorkspaceTokenProvider>
                    <AuthProvider>
                      <WorkspaceProvider>{children}</WorkspaceProvider>
                    </AuthProvider>
                  </WorkspaceTokenProvider>
                </AuthTokenProvider>
              </AppRouterCacheProvider>
              {ReactQueryDevtools ? <ReactQueryDevtools initialIsOpen={false} /> : null}
            </QueryClientProvider>
          </Suspense>
        </PwaInstallProvider>
      </SnackbarProvider>
    </ThemeProvider>
  )
}
