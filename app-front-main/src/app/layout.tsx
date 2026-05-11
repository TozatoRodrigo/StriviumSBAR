'use client'

import '@/lib/i18n'
import { AppRouterCacheProvider } from '@mui/material-nextjs/v15-appRouter'
import { Roboto } from 'next/font/google'
import './globals.css'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { Suspense, useEffect } from 'react'
import { Loader } from '@/components/Loader'
import { SnackbarProvider } from 'notistack'
import { AuthTokenProvider } from '@/contexts/AuthTokenContext'
import { AuthProvider } from '@/contexts/AuthContext'
import { WorkspaceTokenProvider } from '@/contexts/WorkspaceTokenContext'
import { WorkspaceProvider } from '@/contexts/WorkspaceContext'
import { createTheme, ThemeProvider } from '@mui/material'
import { PwaInstallProvider } from '@/components/PwaInstallProvider'

const roboto = Roboto({
  subsets: ['latin'],
})

const theme = createTheme({
  colorSchemes: {
    dark: false,
  },
})

const queryClient = new QueryClient()

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  useEffect(() => {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js').then(registration => console.log('scope is: ', registration.scope))
    }
  }, [])

  return (
    <html lang="pt_BR" className={roboto.className}>
      <head>
        <title>Strivium - Link</title>
        <link rel="manifest" href="/manifest.json" />
      </head>
      <body className={`antialiased`}>
        <div className="container mx-auto max-w-5xl h-[100dvh]">
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
                    <ReactQueryDevtools initialIsOpen={false} />
                  </QueryClientProvider>
                </Suspense>
              </PwaInstallProvider>
            </SnackbarProvider>
          </ThemeProvider>
        </div>
      </body>
    </html>
  )
}
