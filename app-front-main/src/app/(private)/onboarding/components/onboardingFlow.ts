export const onboardingSteps = [
  'workspace',
  'team',
  'invite',
  'patient',
  'hospitalization',
  'success',
] as const

export type OnboardingStep = (typeof onboardingSteps)[number]

type OnboardingEligibilityInput = {
  workspaceCount: number
  pendingInvitesCount: number
}

const progressByStep: Record<OnboardingStep, number> = {
  workspace: 20,
  team: 40,
  invite: 60,
  patient: 80,
  hospitalization: 100,
  success: 100,
}

export const getOnboardingProgress = (step: OnboardingStep) => progressByStep[step]

export const getOnboardingStepNumber = (step: OnboardingStep) => {
  const index = onboardingSteps.indexOf(step)
  if (index < 0) return 1
  return Math.min(index + 1, 5)
}

export const getNextOnboardingStep = (step: OnboardingStep): OnboardingStep | null => {
  const index = onboardingSteps.indexOf(step)
  if (index < 0 || index >= onboardingSteps.length - 1) return null
  return onboardingSteps[index + 1]
}

export const shouldEnterOnboarding = ({ workspaceCount, pendingInvitesCount }: OnboardingEligibilityInput) =>
  workspaceCount === 0 && pendingInvitesCount === 0
