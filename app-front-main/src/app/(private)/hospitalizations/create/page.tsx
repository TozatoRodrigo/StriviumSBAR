'use client'

import { Box, Stack } from '@mui/material'
import { useMemo, useState } from 'react'

import { useRouter } from 'next/navigation'
import { HOSPITALIZATIONS } from '@/routes'
import { BottomBar } from '@/components/BottomBar'
import { TopBar } from '@/components/TopBar'
import { PatientStep } from './components/PatientStep'
import { HospitalizationStep } from './components/HospitalizationStep'
import { HospitalizationForm } from '../(hospitalization_id)/components/HospitalizationForm'

enum StepEnum {
  patient = 'patient',
  hospitalization = 'hospitalization',
}

export default function Create() {
  const [step, setStep] = useState<StepEnum>(StepEnum.patient)
  const [selectedId, setSelectedId] = useState('')
  const router = useRouter()

  const actions = useMemo(
    () => ({
      [StepEnum.patient]: {
        back: () => router.push(HOSPITALIZATIONS.PENDINGS),
        next: () => setStep(StepEnum.hospitalization),
        can: { next: !!selectedId },
        label: 'Avançar',
      },
      [StepEnum.hospitalization]: {
        back: () => setStep(StepEnum.patient),
        next: () => {
          const form = document.getElementById(HospitalizationForm.id) as HTMLFormElement
          form?.requestSubmit()
        },
        can: { next: true },
        label: 'Salvar',
      },
    }),
    [router, selectedId]
  )

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
      <TopBar>
        <TopBar.Back href={HOSPITALIZATIONS.PENDINGS} />
        <TopBar.Title>Cadastrar internação</TopBar.Title>
      </TopBar>
      <Stack className="p-4" flex={1}>
        {step === StepEnum.patient && (
          <PatientStep selectedId={selectedId} onSelect={(id: string) => setSelectedId(id)} />
        )}
        {step === StepEnum.hospitalization && <HospitalizationStep selectedId={selectedId} />}
      </Stack>
      <BottomBar>
        <BottomBar.ActionOutlined onClick={actions[step].back}>Voltar</BottomBar.ActionOutlined>
        <BottomBar.ActionContained onClick={actions[step].next} disabled={!actions[step].can.next}>
          {actions[step].label}
        </BottomBar.ActionContained>
      </BottomBar>
    </Box>
  )
}
