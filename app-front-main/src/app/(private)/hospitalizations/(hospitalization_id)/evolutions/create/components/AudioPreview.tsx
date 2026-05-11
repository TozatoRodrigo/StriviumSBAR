import { Box, Typography } from '@mui/material'

type AudioPreviewProps = {
  audioURL: string
}

export const AudioPreview = ({ audioURL }: AudioPreviewProps) => {
  return (
    <Box>
      <Typography variant="subtitle2" color="text.secondary" mb={1}>
        Prévia da Gravação:
      </Typography>

      <audio controls src={audioURL} style={{ width: '100%' }} />
    </Box>
  )
}
