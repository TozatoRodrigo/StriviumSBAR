import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { EvolutionForm } from '../EvolutionForm'

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
}

const uninstallSpeechRecognitionMock = () => {
  Object.defineProperty(window, 'SpeechRecognition', {
    configurable: true,
    writable: true,
    value: undefined,
  })
}

const requiredInitialData = {
  type: 'hospitalization_visit' as const,
  situation: 'Paciente em avaliação',
  assessment: 'Paciente clinicamente estável',
  recommendation: 'Manter observação clínica',
  priority: 'routine' as const,
}

describe('EvolutionForm voice dictation', () => {
  beforeEach(() => {
    MockSpeechRecognition.instances = []
    installSpeechRecognitionMock()
  })

  afterEach(() => {
    uninstallSpeechRecognitionMock()
    vi.unstubAllEnvs()
    vi.clearAllMocks()
  })

  it('does not render dictation buttons when the feature flag is disabled', () => {
    vi.stubEnv('NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION', 'false')

    render(<EvolutionForm isPending={false} submitAction={vi.fn()} initialData={requiredInitialData} />)

    expect(screen.queryAllByRole('button', { name: /Ditar por voz/ })).toHaveLength(0)
  })

  it('renders one dictation button for each textual SBAR field when enabled', () => {
    vi.stubEnv('NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION', 'true')

    render(<EvolutionForm isPending={false} submitAction={vi.fn()} initialData={requiredInitialData} />)

    expect(screen.getAllByRole('button', { name: /Ditar por voz/ })).toHaveLength(7)
  })

  it('appends the transcript to the selected field without replacing existing text', async () => {
    vi.stubEnv('NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION', 'true')
    const user = userEvent.setup()

    render(<EvolutionForm isPending={false} submitAction={vi.fn()} initialData={requiredInitialData} />)

    await user.click(screen.getByRole('button', { name: 'Ditar por voz em Situação atual' }))
    expect(MockSpeechRecognition.instances[0].continuous).toBe(true)
    await act(async () => {
      MockSpeechRecognition.instances[0].emitResult('sem febre nas últimas horas')
    })

    await waitFor(() =>
      expect(screen.getByLabelText('Situação atual')).toHaveValue(
        'Paciente em avaliação sem febre nas últimas horas'
      )
    )
    await waitFor(() =>
      expect(screen.getByLabelText('Avaliação clínica')).toHaveValue('Paciente clinicamente estável')
    )
  })

  it('uses continuous dictation for the main SBAR fields', async () => {
    vi.stubEnv('NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION', 'true')
    const user = userEvent.setup()

    render(<EvolutionForm isPending={false} submitAction={vi.fn()} initialData={requiredInitialData} />)

    const fieldCases = [
      {
        buttonName: 'Ditar por voz em Situação atual',
        fieldLabel: 'Situação atual',
        initialValue: 'Paciente em avaliação',
        transcript: 'sem febre',
      },
      {
        buttonName: 'Ditar por voz em Contexto clínico relevante',
        fieldLabel: 'Contexto clínico relevante',
        initialValue: '',
        transcript: 'internado por pneumonia',
      },
      {
        buttonName: 'Ditar por voz em Avaliação clínica',
        fieldLabel: 'Avaliação clínica',
        initialValue: 'Paciente clinicamente estável',
        transcript: 'melhora parcial',
      },
      {
        buttonName: 'Ditar por voz em Recomendação',
        fieldLabel: 'Recomendação',
        initialValue: 'Manter observação clínica',
        transcript: 'reavaliar amanhã',
      },
    ]

    for (const fieldCase of fieldCases) {
      const instanceIndex = MockSpeechRecognition.instances.length

      await user.click(screen.getByRole('button', { name: fieldCase.buttonName }))

      expect(MockSpeechRecognition.instances[instanceIndex].continuous).toBe(true)

      await act(async () => {
        MockSpeechRecognition.instances[instanceIndex].emitResult(fieldCase.transcript)
      })

      const expectedValue = [fieldCase.initialValue, fieldCase.transcript].filter(Boolean).join(' ')
      await waitFor(() =>
        expect(screen.getByLabelText(fieldCase.fieldLabel)).toHaveValue(expectedValue)
      )
    }
  })

  it('does not add audio files to the submit payload', async () => {
    vi.stubEnv('NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION', 'true')
    const submitAction = vi.fn()

    render(<EvolutionForm isPending={false} submitAction={submitAction} initialData={requiredInitialData} />)

    fireEvent.submit(document.getElementById(EvolutionForm.id)!)

    await waitFor(() => expect(submitAction).toHaveBeenCalledTimes(1))
    const payload = submitAction.mock.calls[0][0] as FormData
    expect(payload.get('files')).toBeNull()
    expect(payload.get('sbar_situation')).toBe('Paciente em avaliação')
    expect(payload.get('action_type')).toBe('hospitalization_visit')
  })

  it('submits hospitalization_discharge when outcome is Alta hospitalar', async () => {
    vi.stubEnv('NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION', 'false')
    const submitAction = vi.fn()
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    const user = userEvent.setup()

    render(<EvolutionForm isPending={false} submitAction={submitAction} initialData={requiredInitialData} />)

    await user.click(screen.getByRole('combobox', { name: 'Desfecho da internação' }))
    await user.click(screen.getByRole('option', { name: 'Alta hospitalar' }))
    fireEvent.submit(document.getElementById(EvolutionForm.id)!)

    await waitFor(() => expect(submitAction).toHaveBeenCalledTimes(1))
    const payload = submitAction.mock.calls[0][0] as FormData
    expect(payload.get('action_type')).toBe('hospitalization_discharge')
  })

  it('submits hospitalization_deceased when outcome is Óbito', async () => {
    vi.stubEnv('NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION', 'false')
    const submitAction = vi.fn()
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    const user = userEvent.setup()

    render(<EvolutionForm isPending={false} submitAction={submitAction} initialData={requiredInitialData} />)

    await user.click(screen.getByRole('combobox', { name: 'Desfecho da internação' }))
    await user.click(screen.getByRole('option', { name: 'Óbito' }))
    fireEvent.submit(document.getElementById(EvolutionForm.id)!)

    await waitFor(() => expect(submitAction).toHaveBeenCalledTimes(1))
    const payload = submitAction.mock.calls[0][0] as FormData
    expect(payload.get('action_type')).toBe('hospitalization_deceased')
  })

  it('does not submit when closing outcome is not confirmed', async () => {
    vi.stubEnv('NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION', 'false')
    const submitAction = vi.fn()
    const confirmSpy = vi.spyOn(window, 'confirm').mockReturnValue(false)
    const user = userEvent.setup()

    render(<EvolutionForm isPending={false} submitAction={submitAction} initialData={requiredInitialData} />)

    await user.click(screen.getByRole('combobox', { name: 'Desfecho da internação' }))
    await user.click(screen.getByRole('option', { name: 'Alta hospitalar' }))
    fireEvent.submit(document.getElementById(EvolutionForm.id)!)

    await waitFor(() => expect(confirmSpy).toHaveBeenCalledTimes(1))
    expect(submitAction).not.toHaveBeenCalled()
  })

  it('keeps outcome selector disabled when editing evolution', () => {
    vi.stubEnv('NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION', 'false')

    render(
      <EvolutionForm
        isPending={false}
        submitAction={vi.fn()}
        initialData={requiredInitialData}
        allowOutcomeSelection={false}
      />
    )

    expect(screen.getByRole('combobox', { name: 'Desfecho da internação' })).toHaveAttribute(
      'aria-disabled',
      'true'
    )
  })
})
