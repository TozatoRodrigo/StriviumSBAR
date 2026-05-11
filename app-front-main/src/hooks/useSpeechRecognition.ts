'use client'

import { useCallback, useEffect, useRef, useState } from 'react'

type UseSpeechRecognitionParams = {
  lang?: string
  onTranscript: (transcript: string) => void
}

const DEFAULT_ERROR_MESSAGE = 'Não foi possível usar o ditado agora.'
const UNSUPPORTED_MESSAGE = 'Ditado indisponível neste navegador'

const getSpeechRecognitionConstructor = () => {
  if (typeof window === 'undefined') return undefined

  return window.SpeechRecognition ?? window.webkitSpeechRecognition
}

const mapSpeechRecognitionError = (error?: string) => {
  if (error === 'not-allowed' || error === 'service-not-allowed') {
    return 'Permissão do microfone negada.'
  }

  if (error === 'no-speech') {
    return 'Nenhuma fala foi identificada.'
  }

  if (error === 'audio-capture') {
    return 'Microfone indisponível.'
  }

  if (error === 'network') {
    return 'Ditado indisponível: verifique sua conexão com a internet. O Chrome usa servidores do Google para reconhecimento de fala.'
  }

  return DEFAULT_ERROR_MESSAGE
}

export const useSpeechRecognition = ({
  lang = 'pt-BR',
  onTranscript,
}: UseSpeechRecognitionParams) => {
  const recognitionRef = useRef<BrowserSpeechRecognition | null>(null)
  const [status, setStatus] = useState<SpeechRecognitionStatus>('idle')
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [isSupported, setIsSupported] = useState(false)

  useEffect(() => {
    setIsSupported(Boolean(getSpeechRecognitionConstructor()))
  }, [])

  const stop = useCallback(() => {
    recognitionRef.current?.stop()
    recognitionRef.current = null
    setStatus('idle')
  }, [])

  const start = useCallback(() => {
    const Recognition = getSpeechRecognitionConstructor()

    if (!Recognition) {
      setErrorMessage(UNSUPPORTED_MESSAGE)
      setStatus('error')
      return
    }

    recognitionRef.current?.abort()

    const recognition = new Recognition()
    recognition.continuous = false
    recognition.interimResults = true
    recognition.lang = lang

    recognition.onstart = () => {
      setErrorMessage(null)
      setStatus('listening')
    }

    recognition.onresult = event => {
      let transcript = ''
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i]
        if (result.isFinal) {
          transcript += result[0]?.transcript ?? ''
        }
      }
      transcript = transcript.trim()

      if (!transcript) return

      setStatus('transcribing')
      onTranscript(transcript)
      setStatus('idle')
    }

    recognition.onerror = event => {
      setErrorMessage(mapSpeechRecognitionError(event.error))
      setStatus('error')
    }

    recognition.onend = () => {
      recognitionRef.current = null
      setStatus(currentStatus =>
        currentStatus === 'listening' || currentStatus === 'transcribing'
          ? 'idle'
          : currentStatus
      )
    }

    recognitionRef.current = recognition
    recognition.start()
  }, [lang, onTranscript])

  useEffect(
    () => () => {
      recognitionRef.current?.abort()
      recognitionRef.current = null
    },
    []
  )

  return {
    errorMessage,
    isSupported,
    start,
    status,
    stop,
  }
}

export const speechRecognitionUnsupportedMessage = UNSUPPORTED_MESSAGE
