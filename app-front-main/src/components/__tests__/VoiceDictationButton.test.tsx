import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { VoiceDictationButton } from '@/components/VoiceDictationButton'

class MockSpeechRecognition implements BrowserSpeechRecognition {
  static instances: MockSpeechRecognition[] = []

  continuous = false
  interimResults = false
  lang = ''
  onend: ((event: Event) => void) | null = null
  onerror: ((event: SpeechRecognitionErrorEvent) => void) | null = null
  onresult: ((event: SpeechRecognitionEvent) => void) | null = null
  onstart: ((event: Event) => void) | null = null
  abort = vi.fn()
  stop = vi.fn(() => this.onend?.(new Event('end')))
  start = vi.fn(() => this.onstart?.(new Event('start')))

  constructor() {
    MockSpeechRecognition.instances.push(this)
  }

  emitResult(transcript: string) {
    this.onresult?.({
      resultIndex: 0,
      results: {
        length: 1,
        0: {
          isFinal: true,
          0: { transcript },
        },
      },
    } as SpeechRecognitionEvent)
  }

  emitError(error: string) {
    this.onerror?.({ error } as SpeechRecognitionErrorEvent)
  }
}

const installSpeechRecognitionMock = () => {
  Object.defineProperty(window, 'SpeechRecognition', {
    configurable: true,
    writable: true,
    value: MockSpeechRecognition,
  })
  Object.defineProperty(window, 'webkitSpeechRecognition', {
    configurable: true,
    writable: true,
    value: undefined,
  })
}

const uninstallSpeechRecognitionMock = () => {
  Object.defineProperty(window, 'SpeechRecognition', {
    configurable: true,
    writable: true,
    value: undefined,
  })
  Object.defineProperty(window, 'webkitSpeechRecognition', {
    configurable: true,
    writable: true,
    value: undefined,
  })
}

describe('VoiceDictationButton', () => {
  beforeEach(() => {
    MockSpeechRecognition.instances = []
    installSpeechRecognitionMock()
  })

  afterEach(() => {
    uninstallSpeechRecognitionMock()
    vi.clearAllMocks()
  })

  it('starts speech recognition and returns final transcript', async () => {
    const onTranscript = vi.fn()
    const user = userEvent.setup()

    render(<VoiceDictationButton fieldLabel="Situação atual" onTranscript={onTranscript} />)

    await user.click(screen.getByRole('button', { name: 'Ditar por voz em Situação atual' }))

    expect(MockSpeechRecognition.instances[0].lang).toBe('pt-BR')
    expect(MockSpeechRecognition.instances[0].start).toHaveBeenCalledTimes(1)
    expect(screen.getByRole('button', { name: 'Parar ditado em Situação atual' })).toBeInTheDocument()

    act(() => {
      MockSpeechRecognition.instances[0].emitResult('paciente estável')
    })

    expect(onTranscript).toHaveBeenCalledWith('paciente estável')
  })

  it('is disabled when the browser does not support speech recognition', () => {
    uninstallSpeechRecognitionMock()

    render(<VoiceDictationButton fieldLabel="Contexto" onTranscript={vi.fn()} />)

    expect(screen.getByRole('button', { name: 'Ditado indisponível neste navegador' })).toBeDisabled()
  })

  it('shows a friendly error after permission is denied', async () => {
    const user = userEvent.setup()

    render(<VoiceDictationButton fieldLabel="Avaliação" onTranscript={vi.fn()} />)

    await user.click(screen.getByRole('button', { name: 'Ditar por voz em Avaliação' }))
    act(() => {
      MockSpeechRecognition.instances[0].emitError('not-allowed')
    })

    expect(
      screen.getByRole('button', {
        name: /Permissão do microfone\/ditado negada\./,
      })
    ).toBeInTheDocument()
  })
})
