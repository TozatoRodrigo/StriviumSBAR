'use client'

import Stack from '@mui/material/Stack'
import dynamic from 'next/dynamic'
import { useRouter } from 'next/navigation'
import { useState } from 'react'

import { OnboardingProgress } from './OnboardingProgress'
import { OnboardingStep, getNextOnboardingStep } from './onboardingFlow'
import { WorkspaceStep } from './steps/WorkspaceStep'

const TeamStep = dynamic(() => import('./steps/TeamStep').then(module => module.TeamStep), {
  ssr: false,
})
const InviteStep = dynamic(() => import('./steps/InviteStep').then(module => module.InviteStep), {
  ssr: false,
})
const PatientStep = dynamic(() => import('./steps/PatientStep').then(module => module.PatientStep), {
  ssr: false,
})
const HospitalizationStep = dynamic(
  () => import('./steps/HospitalizationStep').then(module => module.HospitalizationStep),
  { ssr: false }
)
const SuccessStep = dynamic(() => import('./steps/SuccessStep').then(module => module.SuccessStep), {
  ssr: false,
})

type SummaryState = {
  workspaceName: string
  teamName: string
  inviteCount: number
  patientName: string
  hospitalizationInfo: {
    place: string
    sector: string
  }
}

const defaultSummary: SummaryState = {
  workspaceName: '',
  teamName: '',
  inviteCount: 0,
  patientName: '',
  hospitalizationInfo: {
    place: '',
    sector: '',
  },
}

export const OnboardingWizard = () => {
  const router = useRouter()
  const [step, setStep] = useState<OnboardingStep>('workspace')
  const [summary, setSummary] = useState<SummaryState>(defaultSummary)
  const [createdIds, setCreatedIds] = useState<{
    tenantId: string | null
    teamId: string | null
    patientId: string | null
  }>({
    tenantId: null,
    teamId: null,
    patientId: null,
  })

  const goNext = () => {
    const nextStep = getNextOnboardingStep(step)
    if (nextStep) setStep(nextStep)
  }

  return (
    <Stack sx={{ minHeight: '100dvh', backgroundColor: '#fff' }}>
      <Stack className="p-4 pb-2">
        <OnboardingProgress step={step} />
      </Stack>

      {step === 'workspace' && (
        <WorkspaceStep
          onCompleted={({ tenantId, workspaceName }) => {
            setCreatedIds(current => ({ ...current, tenantId }))
            setSummary(current => ({ ...current, workspaceName }))
            goNext()
          }}
        />
      )}

      {step === 'team' && (
        <TeamStep
          onCompleted={({ teamId, teamName }) => {
            setCreatedIds(current => ({ ...current, teamId }))
            setSummary(current => ({ ...current, teamName }))
            goNext()
          }}
        />
      )}

      {step === 'invite' && (
        <InviteStep
          onCompleted={({ inviteCount }) => {
            setSummary(current => ({ ...current, inviteCount }))
            goNext()
          }}
        />
      )}

      {step === 'patient' && (
        <PatientStep
          onCompleted={({ patientId, patientName }) => {
            setCreatedIds(current => ({ ...current, patientId }))
            setSummary(current => ({ ...current, patientName }))
            goNext()
          }}
        />
      )}

      {step === 'hospitalization' && createdIds.teamId && createdIds.patientId && (
        <HospitalizationStep
          teamId={createdIds.teamId}
          patientId={createdIds.patientId}
          onCompleted={({ place, sector }) => {
            setSummary(current => ({
              ...current,
              hospitalizationInfo: { place, sector },
            }))
            goNext()
          }}
        />
      )}

      {step === 'success' && (
        <SuccessStep summary={summary} onComplete={() => router.replace('/hospitalizations/pendings')} />
      )}
    </Stack>
  )
}
