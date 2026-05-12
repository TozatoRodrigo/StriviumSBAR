import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import type { ReactElement } from 'react'
import { afterEach, describe, expect, it, vi } from 'vitest'

import api from '@/api/axios'
import { EvolutionForm } from '../EvolutionForm'

vi.mock('@/api/axios', () => ({
  default: {
    post: vi.fn(),
  },
}))

const requiredInitialData = {
  type: 'hospitalization_visit' as const,
  situation: 'Paciente em avaliação',
  assessment: 'Paciente clinicamente estável',
  recommendation: 'Manter observação clínica',
  priority: 'routine' as const,
}

const renderWithQueryClient = (ui: ReactElement) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  })

  return render(<QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>)
}

describe('EvolutionForm AI dictation', () => {
  afterEach(() => {
    vi.unstubAllEnvs()
    vi.clearAllMocks()
  })

  it('applies AI SBAR draft and requires medical review before submit', async () => {
    vi.stubEnv('NEXT_PUBLIC_EXPERIMENTAL_SBAR_AI_DICTATION', 'true')
    vi.mocked(api.post).mockResolvedValueOnce({
      data: {
        situation: 'Paciente sem febre.',
        background: '',
        assessment: 'Evolução estável.',
        recommendation: 'Manter conduta.',
        plan: 'Reavaliar amanhã.',
        missing_information: ['Sinais vitais completos.'],
        warnings: ['Revise o texto antes de salvar.'],
        confidence: {
          situation: 0.91,
          background: 0,
          assessment: 0.82,
          recommendation: 0.74,
          plan: 0.73,
        },
      },
    })
    const submitAction = vi.fn()
    const user = userEvent.setup()

    renderWithQueryClient(
      <EvolutionForm
        isPending={false}
        submitAction={submitAction}
        initialData={requiredInitialData}
        hospitalizationId="hospitalization-1"
      />
    )

    await user.clear(screen.getByLabelText('Texto bruto do ditado'))
    await user.type(
      screen.getByLabelText('Texto bruto do ditado'),
      'paciente sem febre evolução estável manter conduta reavaliar amanhã'
    )
    await user.click(screen.getByRole('button', { name: 'Organizar em SBAR' }))

    await waitFor(() => {
      expect(screen.getByLabelText('Situação atual')).toHaveValue('Paciente sem febre.')
    })
    expect(screen.getByLabelText('Avaliação clínica')).toHaveValue('Evolução estável.')
    expect(screen.getByLabelText('Recomendação')).toHaveValue('Manter conduta.')
    expect(screen.getByLabelText('Plano')).toHaveValue('Reavaliar amanhã.')
    expect(screen.getByText('Sinais vitais completos.')).toBeInTheDocument()
    expect(screen.getByText('Revise o texto antes de salvar.')).toBeInTheDocument()

    fireEvent.submit(document.getElementById(EvolutionForm.id)!)

    expect(submitAction).not.toHaveBeenCalled()
    expect(screen.getByText('Confirme a revisão médica antes de salvar.')).toBeInTheDocument()

    await user.click(screen.getByRole('checkbox', { name: 'Revisei e confirmo o rascunho gerado pela IA' }))
    fireEvent.submit(document.getElementById(EvolutionForm.id)!)

    await waitFor(() => expect(submitAction).toHaveBeenCalledTimes(1))
    const payload = submitAction.mock.calls[0][0] as FormData
    expect(payload.get('sbar_ai_generated')).toBe('true')
    expect(payload.get('sbar_ai_review_confirmed')).toBe('true')
    expect(payload.get('sbar_source_transcript')).toBe(
      'paciente sem febre evolução estável manter conduta reavaliar amanhã'
    )
    expect(payload.get('sbar_plan')).toBe('Reavaliar amanhã.')
  })
})
