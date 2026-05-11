import { Box } from '@mui/material'
import { keyframes } from '@emotion/react'

const heartbeat = keyframes`
  0% { transform: scale(1); }
  14% { transform: scale(1.3); }
  28% { transform: scale(1); }
  42% { transform: scale(1.3); }
  70% { transform: scale(1); }
  100% { transform: scale(1); }
`

export const Loader = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100dvh',
      }}
    >
      <Box
        component="img"
        src="/logo.svg"
        alt="Loading..."
        sx={{
          width: 64,
          height: 64,
          animation: `${heartbeat} 1.5s ease-in-out infinite`,
        }}
      />
    </Box>
  )
}
