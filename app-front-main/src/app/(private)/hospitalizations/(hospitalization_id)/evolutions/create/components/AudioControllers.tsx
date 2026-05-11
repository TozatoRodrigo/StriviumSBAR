'use client'

import { Button, IconButton, Stack } from '@mui/material'
import MicIcon from '@mui/icons-material/Mic'
import StopIcon from '@mui/icons-material/Stop'
import RestartAltIcon from '@mui/icons-material/RestartAlt'
import { AudioRecord } from '@/hooks/useAudioRecorder'

type AudioControllersProps = { hasBlob: boolean; disabled?: boolean } & Pick<
  AudioRecord,
  'isRecording' | 'startRecording' | 'stopRecording' | 'resetRecording'
>

export const AudioControllers = ({
  isRecording,
  startRecording,
  stopRecording,
  resetRecording,
  hasBlob,
  disabled = false,
}: AudioControllersProps) => {
  return (
    <Stack direction="row" gap={1} alignItems="center">
      {!isRecording ? (
        <Button
          fullWidth
          variant="contained"
          color="primary"
          startIcon={<MicIcon />}
          onClick={startRecording}
          sx={{ borderRadius: '999px' }}
          disabled={disabled}
        >
          Gravar
        </Button>
      ) : (
        <Button
          fullWidth
          variant="outlined"
          color="error"
          startIcon={<StopIcon />}
          onClick={stopRecording}
          sx={{ borderRadius: '999px' }}
          disabled={disabled}
        >
          Parar
        </Button>
      )}

      {hasBlob && (
        <IconButton onClick={resetRecording} color="warning" disabled={disabled}>
          <RestartAltIcon />
        </IconButton>
      )}
    </Stack>
  )
}
