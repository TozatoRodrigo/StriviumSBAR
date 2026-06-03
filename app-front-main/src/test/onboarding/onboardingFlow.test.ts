import { describe, expect, it } from 'vitest'

import {
  getNextOnboardingStep,
  getOnboardingProgress,
  getOnboardingStepNumber,
  shouldEnterOnboarding,
} from '@/app/(private)/onboarding/components/onboardingFlow'

describe('onboardingFlow', () => {
  it('returns the right progress for each step', () => {
    expect(getOnboardingProgress('workspace')).toBe(20)
    expect(getOnboardingProgress('team')).toBe(40)
    expect(getOnboardingProgress('invite')).toBe(60)
    expect(getOnboardingProgress('patient')).toBe(80)
    expect(getOnboardingProgress('hospitalization')).toBe(100)
    expect(getOnboardingProgress('success')).toBe(100)
  })

  it('returns the next step in sequence', () => {
    expect(getNextOnboardingStep('workspace')).toBe('team')
    expect(getNextOnboardingStep('team')).toBe('invite')
    expect(getNextOnboardingStep('invite')).toBe('patient')
    expect(getNextOnboardingStep('patient')).toBe('hospitalization')
    expect(getNextOnboardingStep('hospitalization')).toBe('success')
    expect(getNextOnboardingStep('success')).toBeNull()
  })

  it('returns the expected displayed step number', () => {
    expect(getOnboardingStepNumber('workspace')).toBe(1)
    expect(getOnboardingStepNumber('team')).toBe(2)
    expect(getOnboardingStepNumber('invite')).toBe(3)
    expect(getOnboardingStepNumber('patient')).toBe(4)
    expect(getOnboardingStepNumber('hospitalization')).toBe(5)
    expect(getOnboardingStepNumber('success')).toBe(5)
  })

  it('enables onboarding only when there are no workspaces and no pending invites', () => {
    expect(shouldEnterOnboarding({ workspaceCount: 0, pendingInvitesCount: 0 })).toBe(true)
    expect(shouldEnterOnboarding({ workspaceCount: 1, pendingInvitesCount: 0 })).toBe(false)
    expect(shouldEnterOnboarding({ workspaceCount: 0, pendingInvitesCount: 1 })).toBe(false)
    expect(shouldEnterOnboarding({ workspaceCount: 2, pendingInvitesCount: 3 })).toBe(false)
  })
})
