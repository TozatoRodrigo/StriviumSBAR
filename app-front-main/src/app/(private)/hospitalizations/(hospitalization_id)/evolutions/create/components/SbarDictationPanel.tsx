'use client'

import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh'
import MicIcon from '@mui/icons-material/Mic'
import StopIcon from '@mui/icons-material/Stop'
import { Alert, Box, Button, Chip, Stack, TextField, Typography } from '@mui/material'
import { useCallback, useState } from 'react'

import { useExtractSbar } from '@/hooks/mutations/sbar'
import type { SbarExtractResponse } from '@/hooks/mutations/sbar'
import { speechRecognitionUnsupportedMessage, useSpeechRecognition } from '@/hooks/useSpeechRecognition'

type SbarDictationPanelProps = {
  disabled?: boolean
  hospitalizationId?: string
  onApply: (result: SbarExtractResponse, sourceTranscript: string) => void
}

const appendTranscript = (current: string, transcript: string) =>
  [current.trim(), transcript.trim()].filter(Boolean).join(' ').replace(/\s+/g, ' ')

export const SbarDictationPanel = ({
  disabled = false,
  hospitalizationId,
  onApply,
}: SbarDictationPanelProps) => {
  const [transcript, setTranscript] = useState('')
  const [lastResult, setLastResult] = useState<SbarExtractResponse | null>(null)
  const [localError, setLocalError] = useState<string | null>(null)
  const extractSbar = useExtractSbar()

  const handleTranscript = useCallback((finalTranscript: string) => {
    setTranscript(current => appendTranscript(current, finalTranscript))
  }, [])

  const { errorMessage, interimTranscript, isSupported, start, status, stop } = useSpeechRecognition({
    continuous: true,
    onTranscript: handleTranscript,
  })

  const isListening = status === 'listening' || status === 'transcribing'
  const isExtracting = extractSbar.isPending
  const hasTranscript = transcript.trim().length > 0

  const handleToggleRecording = () => {
    if (isListening) {
      stop()
      return
    }

    start()
  }

  const handleExtract = async () => {
    const sourceTranscript = transcript.trim()
    if (!sourceTranscript) {
      setLocalError('Digite ou dite a evolução antes de organizar em SBAR.')
      return
    }

    setLocalError(null)
    try {
      const result = await extractSbar.mutateAsync({
        transcript: sourceTranscript,
        context: hospitalizationId ? { hospitalization_id: hospitalizationId } : undefined,
      })
      setLastResult(result)
      onApply(result, sourceTranscript)
    } catch {
      setLocalError('Não foi possível organizar o ditado agora. O texto bruto continua disponível.')
    }
  }

  return (
    <Box
      sx={{
        border: theme => `1px solid ${theme.palette.divider}`,
        borderRadius: 2,
        p: { xs: 2, sm: 2.5 },
        bgcolor: 'background.paper',
      }}
    >
      <Stack gap={2}>
        <Box>
          <Stack direction="row" alignItems="center" justifyContent="space-between" gap={1}>
            <Box>
              <Typography fontWeight={700} color="text.primary">
                Ditado livre
              </Typography>
              <Typography fontSize={13} color="text.secondary">
                Transcrição bruta preservada para auditoria.
              </Typography>
            </Box>
            <Chip label="Rascunho" size="small" color="warning" variant="outlined" />
          </Stack>
        </Box>

        <Stack direction={{ xs: 'column', sm: 'row' }} gap={1}>
          <Button
            aria-label={isListening ? 'Parar ditado livre' : 'Iniciar ditado livre'}
            disabled={disabled || !isSupported || isExtracting}
            onClick={handleToggleRecording}
            startIcon={isListening ? <StopIcon /> : <MicIcon />}
            variant={isListening ? 'contained' : 'outlined'}
          >
            {isListening ? 'Parar' : 'Ditar'}
          </Button>
          <Button
            aria-label="Organizar em SBAR"
            disabled={disabled || isExtracting || !hasTranscript}
            onClick={handleExtract}
            startIcon={<AutoFixHighIcon />}
            variant="contained"
          >
            {isExtracting ? 'Organizando...' : 'Organizar em SBAR'}
          </Button>
        </Stack>

        {!isSupported && <Alert severity="warning">{speechRecognitionUnsupportedMessage}</Alert>}
        {errorMessage && <Alert severity="warning">{errorMessage}</Alert>}
        {localError && <Alert severity="warning">{localError}</Alert>}
        <TextField
          disabled={disabled || isExtracting}
          label="Texto bruto do ditado"
          minRows={5}
          multiline
          onChange={event => setTranscript(event.target.value)}
          value={transcript}
          variant="filled"
        />

        {interimTranscript && (
          <Typography fontSize={13} color="text.secondary">
            Ouvindo: {interimTranscript}
          </Typography>
        )}

        {!!lastResult?.warnings.length && (
          <Alert severity="warning">
            <Stack gap={0.5}>
              {lastResult.warnings.map(item => (
                <span key={item}>{item}</span>
              ))}
            </Stack>
          </Alert>
        )}

        {!!lastResult?.missing_information.length && (
          <Alert severity="info">
            <Stack gap={0.5}>
              {lastResult.missing_information.map(item => (
                <span key={item}>{item}</span>
              ))}
            </Stack>
          </Alert>
        )}
      </Stack>
    </Box>
  )
}
