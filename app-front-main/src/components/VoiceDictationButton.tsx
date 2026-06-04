'use client'

import MicIcon from '@mui/icons-material/Mic'
import MicOffIcon from '@mui/icons-material/MicOff'
import StopIcon from '@mui/icons-material/Stop'
import { IconButton, Tooltip } from '@mui/material'

import {
  speechRecognitionUnsupportedMessage,
  useSpeechRecognition,
} from '@/hooks/useSpeechRecognition'

type VoiceDictationButtonProps = {
  continuous?: boolean
  disabled?: boolean
  fieldLabel: string
  onTranscript: (transcript: string) => void
}

export const VoiceDictationButton = ({
  continuous = false,
  disabled = false,
  fieldLabel,
  onTranscript,
}: VoiceDictationButtonProps) => {
  const { errorMessage, isSupported, start, status, stop } = useSpeechRecognition({
    continuous,
    onTranscript,
  })
  const isListening = status === 'listening'
  const isDisabled = disabled || !isSupported || status === 'transcribing'

  const ariaLabel = (() => {
    if (!isSupported) return speechRecognitionUnsupportedMessage
    if (errorMessage) return errorMessage
    if (isListening) return `Parar ditado em ${fieldLabel}`
    if (status === 'transcribing') return `Transcrevendo ditado em ${fieldLabel}`
    return `Ditar por voz em ${fieldLabel}`
  })()

  const tooltipTitle = (() => {
    if (!isSupported) return speechRecognitionUnsupportedMessage
    if (errorMessage) return errorMessage
    if (isListening) return 'Parar ditado'
    if (status === 'transcribing') return 'Transcrevendo...'
    return 'Ditar por voz'
  })()

  const handleClick = () => {
    if (isListening) {
      stop()
      return
    }

    start()
  }

  const Icon = !isSupported ? MicOffIcon : isListening ? StopIcon : MicIcon

  return (
    <Tooltip title={tooltipTitle}>
      <span>
        <IconButton
          aria-label={ariaLabel}
          color={isListening ? 'primary' : errorMessage ? 'error' : 'default'}
          disabled={isDisabled}
          edge="end"
          onClick={handleClick}
          size="small"
        >
          <Icon fontSize="small" />
        </IconButton>
      </span>
    </Tooltip>
  )
}
