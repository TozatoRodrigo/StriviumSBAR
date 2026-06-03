import './globals.css'
import { AppProviders } from '@/components/AppProviders'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Strivium - Link',
  manifest: '/manifest.json',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="pt_BR">
      <body className="antialiased">
        <div className="container mx-auto max-w-5xl h-[100dvh]">
          <AppProviders>{children}</AppProviders>
        </div>
      </body>
    </html>
  )
}
