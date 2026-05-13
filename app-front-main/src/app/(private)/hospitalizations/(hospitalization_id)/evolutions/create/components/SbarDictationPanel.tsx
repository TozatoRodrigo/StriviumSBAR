'use client'

import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh'
import ClearIcon from '@mui/icons-material/Clear'
import MicIcon from '@mui/icons-material/Mic'
import StopIcon from '@mui/icons-material/Stop'
import TextSnippetOutlinedIcon from '@mui/icons-material/TextSnippetOutlined'
import VerifiedOutlinedIcon from '@mui/icons-material/VerifiedOutlined'
import {
  Alert,
  Box,
  Button,
  Chip,
  CircularProgress,
  IconButton,
  LinearProgress,
  Stack,
  TextField,
  Tooltip,
  Typography,
} from '@mui/material'
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

const countWords = (value: string) => value.trim().split(/\s+/).filter(Boolean).length

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
  const wordCount = countWords(transcript)
  const characterCount = transcript.trim().length

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
        border: theme => `1px solid ${isListening ? theme.palette.primary.main : theme.palette.divider}`,
        borderRadius: 2,
        overflow: 'hidden',
        bgcolor: 'background.paper',
        boxShadow: theme => (isListening ? `0 0 0 3px ${theme.palette.primary.main}1f` : 'none'),
      }}
    >
      {isExtracting && <LinearProgress />}
      <Stack gap={2} sx={{ p: { xs: 2, sm: 2.5 } }}>
        <Stack direction={{ xs: 'column', sm: 'row' }} alignItems={{ xs: 'stretch', sm: 'flex-start' }} justifyContent="space-between" gap={1.5}>
          <Stack direction="row" gap={1.25} alignItems="flex-start">
            <Box
              sx={{
                alignItems: 'center',
                bgcolor: isListening ? 'primary.main' : 'action.hover',
                borderRadius: 1.5,
                color: isListening ? 'primary.contrastText' : 'text.secondary',
                display: 'flex',
                height: 40,
                justifyContent: 'center',
                width: 40,
              }}
            >
              {isListening ? <MicIcon fontSize="small" /> : <TextSnippetOutlinedIcon fontSize="small" />}
            </Box>
            <Box>
              <Typography fontWeight={800} color="text.primary">
                Ditado livre da evolução
              </Typography>
              <Typography fontSize={13} color="text.secondary">
                Dite naturalmente, revise o texto bruto e organize em SBAR como rascunho.
              </Typography>
            </Box>
          </Stack>
          <Stack direction="row" gap={1} flexWrap="wrap">
            <Chip label={isListening ? 'Ouvindo agora' : 'Pronto para ditar'} size="small" color={isListening ? 'primary' : 'default'} variant={isListening ? 'filled' : 'outlined'} />
            <Chip label="Texto auditável" size="small" color="info" variant="outlined" />
          </Stack>
        </Stack>

        <Stack direction={{ xs: 'column', sm: 'row' }} gap={1} alignItems={{ xs: 'stretch', sm: 'center' }}>
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
            startIcon={isExtracting ? <CircularProgress color="inherit" size={16} /> : <AutoFixHighIcon />}
            variant="contained"
            sx={{ minWidth: 178 }}
          >
            {isExtracting ? 'Organizando...' : 'Organizar em SBAR'}
          </Button>
          <Tooltip title="Limpar texto bruto">
            <span>
              <IconButton
                aria-label="Limpar texto bruto"
                disabled={disabled || isExtracting || !hasTranscript}
                onClick={() => {
                  setTranscript('')
                  setLastResult(null)
                  setLocalError(null)
                }}
              >
                <ClearIcon />
              </IconButton>
            </span>
          </Tooltip>
        </Stack>

        {!isSupported && <Alert severity="warning">{speechRecognitionUnsupportedMessage}</Alert>}
        {errorMessage && <Alert severity="warning">{errorMessage}</Alert>}
        {localError && <Alert severity="warning">{localError}</Alert>}
        <TextField
          disabled={disabled || isExtracting}
          id="sbar-source-transcript"
          name="sbar-source-transcript"
          label="Texto bruto do ditado"
          minRows={5}
          multiline
          onChange={event => setTranscript(event.target.value)}
          placeholder="Ex.: Paciente evoluiu sem febre, nega dor, sem dispneia. Manter antibiótico e reavaliar amanhã..."
          helperText={`${wordCount} palavras · ${characterCount} caracteres · este texto será preservado se o rascunho for salvo`}
          value={transcript}
          variant="filled"
        />

        {interimTranscript && (
          <Box sx={{ borderLeft: 3, borderColor: 'primary.main', pl: 1.5 }}>
            <Typography fontSize={12} fontWeight={700} color="primary.main">
              Ouvindo agora
            </Typography>
            <Typography fontSize={13} color="text.secondary">
              {interimTranscript}
            </Typography>
          </Box>
        )}

        {lastResult && !lastResult.warnings.length && !lastResult.missing_information.length && (
          <Alert icon={<VerifiedOutlinedIcon fontSize="inherit" />} severity="success">
            Rascunho SBAR aplicado aos campos. Revise cada seção antes de salvar.
          </Alert>
        )}

        {!!lastResult?.warnings.length && (
          <Alert severity="warning">
            <Typography fontSize={13} fontWeight={700} sx={{ mb: 0.5 }}>
              Atenções da extração
            </Typography>
            <Stack gap={0.5}>
              {lastResult.warnings.map(item => (
                <span key={item}>{item}</span>
              ))}
            </Stack>
          </Alert>
        )}

        {!!lastResult?.missing_information.length && (
          <Alert severity="info">
            <Typography fontSize={13} fontWeight={700} sx={{ mb: 0.5 }}>
              Informações ausentes ou ambíguas
            </Typography>
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
