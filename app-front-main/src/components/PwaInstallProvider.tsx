'use client'

import { Capacitor } from '@capacitor/core'
import { SnackbarKey, useSnackbar } from 'notistack'
import { PropsWithChildren, useCallback, useEffect, useState } from 'react'
import { PwaInstallActions } from './PwaInstallActions'

type UserChoice = {
  outcome: 'accepted' | 'dismissed'
  platform: string
}

interface BeforeInstallPromptEvent extends Event {
  readonly platforms: string[]
  readonly userChoice: Promise<UserChoice>
  prompt(): Promise<UserChoice>
}

export function PwaInstallProvider({ children }: PropsWithChildren) {
  const { enqueueSnackbar, closeSnackbar } = useSnackbar()
  const [installPrompt, setInstallPrompt] = useState<BeforeInstallPromptEvent | null>(null)
  const isWeb = !Capacitor.isNativePlatform()

  const handleInstallClick = useCallback(
    (key: SnackbarKey) => {
      if (installPrompt) {
        installPrompt.prompt()
        installPrompt.userChoice.then((choiceResult: UserChoice) => {
          if (choiceResult.outcome === 'accepted') {
            console.log('User accepted the install prompt')
          } else {
            console.log('User dismissed the install prompt')
          }
          setInstallPrompt(null)
          closeSnackbar(key)
        })
      }
    },
    [installPrompt, closeSnackbar]
  )

  const handleCloseClick = useCallback(
    (key: SnackbarKey) => {
      sessionStorage.setItem('pwaInstallDismissed', 'true')
      closeSnackbar(key)
    },
    [closeSnackbar]
  )

  useEffect(() => {
    const handleBeforeInstallPrompt = (event: Event) => {
      event.preventDefault()
      setInstallPrompt(event as BeforeInstallPromptEvent)
    }

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt)

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
    }
  }, [])

  useEffect(() => {
    const dismissed = sessionStorage.getItem('pwaInstallDismissed')
    if (dismissed || !isWeb || !installPrompt) {
      return
    }

    enqueueSnackbar('Instalar aplicativo?', {
      variant: 'info',
      persist: true,
      preventDuplicate: true,
      action: key => (
        <PwaInstallActions onInstall={() => handleInstallClick(key)} onClose={() => handleCloseClick(key)} />
      ),
    })
  }, [installPrompt, isWeb, enqueueSnackbar, handleInstallClick, handleCloseClick])

  return children
}
