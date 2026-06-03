import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'

import { OnboardingWizard } from '@/app/(private)/onboarding/components/OnboardingWizard'

const { replace } = vi.hoisted(() => ({
  replace: vi.fn(),
}))

vi.mock('next/navigation', () => ({
  useRouter: () => ({ replace }),
}))

vi.mock('@/app/(private)/onboarding/components/steps/WorkspaceStep', () => ({
  WorkspaceStep: ({ onCompleted }: { onCompleted: (data: { tenantId: string; workspaceName: string }) => void }) => (
    <button onClick={() => onCompleted({ tenantId: 'tenant-1', workspaceName: 'Workspace A' })}>workspace-step</button>
  ),
}))

vi.mock('@/app/(private)/onboarding/components/steps/TeamStep', () => ({
  TeamStep: ({ onCompleted }: { onCompleted: (data: { teamId: string; teamName: string }) => void }) => (
    <button onClick={() => onCompleted({ teamId: 'team-1', teamName: 'Team A' })}>team-step</button>
  ),
}))

vi.mock('@/app/(private)/onboarding/components/steps/InviteStep', () => ({
  InviteStep: ({ onCompleted }: { onCompleted: (data: { inviteCount: number }) => void }) => (
    <button onClick={() => onCompleted({ inviteCount: 0 })}>invite-step</button>
  ),
}))

vi.mock('@/app/(private)/onboarding/components/steps/PatientStep', () => ({
  PatientStep: ({ onCompleted }: { onCompleted: (data: { patientId: string; patientName: string }) => void }) => (
    <button onClick={() => onCompleted({ patientId: 'patient-1', patientName: 'Paciente A' })}>patient-step</button>
  ),
}))

vi.mock('@/app/(private)/onboarding/components/steps/HospitalizationStep', () => ({
  HospitalizationStep: ({ onCompleted }: { onCompleted: (data: { place: string; sector: string }) => void }) => (
    <button onClick={() => onCompleted({ place: 'Hospital X', sector: 'UTI' })}>hospitalization-step</button>
  ),
}))

vi.mock('@/app/(private)/onboarding/components/steps/SuccessStep', () => ({
  SuccessStep: ({ onComplete }: { onComplete: () => void }) => <button onClick={onComplete}>success-step</button>,
}))

describe('OnboardingWizard', () => {
  it('walks through the flow and redirects on completion', async () => {
    const user = userEvent.setup()

    render(<OnboardingWizard />)

    expect(screen.getByRole('button', { name: 'workspace-step' })).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'workspace-step' }))

    expect(screen.getByRole('button', { name: 'team-step' })).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'team-step' }))

    expect(screen.getByRole('button', { name: 'invite-step' })).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'invite-step' }))

    expect(await screen.findByRole('button', { name: 'patient-step' })).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'patient-step' }))

    expect(await screen.findByRole('button', { name: 'hospitalization-step' })).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'hospitalization-step' }))

    expect(screen.getByRole('button', { name: 'success-step' })).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'success-step' }))

    expect(replace).toHaveBeenCalledWith('/hospitalizations/pendings')
  })
})
