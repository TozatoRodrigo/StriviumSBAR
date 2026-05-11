import { ReactNode } from 'react'
import { Button, Card, CardContent, Fade, Typography } from '@mui/material'
import { ErrorOutline } from '@mui/icons-material'

type ErrorStateProps = {
  title?: string
  message?: string
  onRetry?: () => void
  actionLabel?: string
  icon?: ReactNode
}

export function ErrorState({
  title = 'Ops! Algo deu errado',
  message = 'Não conseguimos carregar as informações. Tente novamente.',
  onRetry,
  actionLabel = 'Tentar novamente',
  icon = <ErrorOutline fontSize="large" color="error" />,
}: ErrorStateProps) {
  return (
    <Fade in appear>
      <div className="flex items-center justify-center w-full h-full p-4">
        <Card className="max-w-md w-full shadow-lg rounded-2xl">
          <CardContent className="flex flex-col items-center text-center gap-4 p-6">
            <div className="text-red-500">{icon}</div>
            <Typography variant="h6" gutterBottom>
              {title}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {message}
            </Typography>
            {onRetry && (
              <Button onClick={onRetry} variant="contained" color="error" className="rounded-xl mt-2">
                {actionLabel}
              </Button>
            )}
          </CardContent>
        </Card>
      </div>
    </Fade>
  )
}
