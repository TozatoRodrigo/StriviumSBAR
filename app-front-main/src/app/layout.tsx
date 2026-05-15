import './globals.css'
import { AppProviders } from '@/components/AppProviders'
import type { Metadata } from 'next'
import { Roboto } from 'next/font/google'

const roboto = Roboto({
  subsets: ['latin'],
  weight: ['300', '400', '500', '700'],
  display: 'swap',
})

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
      <body className={`${roboto.className} antialiased`}>
        <div className="container mx-auto max-w-5xl h-[100dvh]">
          <AppProviders>{children}</AppProviders>
        </div>
      </body>
    </html>
  )
}
