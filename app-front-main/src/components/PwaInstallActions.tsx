'use client'

import { Button } from '@mui/material'
import { useTranslation } from 'react-i18next'

interface PwaInstallNotificationProps {
  onInstall: () => void
  onClose: () => void
}

export function PwaInstallActions({ onInstall, onClose }: PwaInstallNotificationProps) {
  const { t } = useTranslation()

  return (
    <div className="flex items-center gap-2 rounded-lg p-2">
      <Button variant="text" color="primary" onClick={onClose} sx={{ color: 'white', fontWeight: 'bold' }}>
        {t('ignore')}
      </Button>
      <Button variant="contained" color="primary" onClick={onInstall} sx={{ color: 'white', fontWeight: 'bold' }}>
        {t('install_app')}
      </Button>
    </div>
  )
}
