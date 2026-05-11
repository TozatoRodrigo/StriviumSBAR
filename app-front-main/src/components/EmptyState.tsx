import { ReactNode } from 'react'
import { Card, CardContent, Typography, Button, Fade } from '@mui/material'
import { InboxOutlined } from '@mui/icons-material'

type EmptyStateProps = {
  title?: string
  message?: string
  actionLabel?: string
  onAction?: () => void
  icon?: ReactNode
}

export function EmptyState({
  title = 'Nenhum dado encontrado',
  message = 'Não há informações disponíveis no momento.',
  actionLabel,
  onAction,
  icon = <InboxOutlined fontSize="large" color="disabled" />,
}: EmptyStateProps) {
  return (
    <Fade in appear>
      <div className="flex items-center justify-center w-full h-full p-4">
        <Card className="max-w-md w-full shadow-lg rounded-2xl">
          <CardContent className="flex flex-col items-center text-center gap-4 p-6">
            <div className="text-gray-400">{icon}</div>
            <Typography variant="h6" gutterBottom>
              {title}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {message}
            </Typography>
            {onAction && actionLabel && (
              <Button onClick={onAction} variant="contained" className="rounded-xl mt-2">
                {actionLabel}
              </Button>
            )}
          </CardContent>
        </Card>
      </div>
    </Fade>
  )
}
