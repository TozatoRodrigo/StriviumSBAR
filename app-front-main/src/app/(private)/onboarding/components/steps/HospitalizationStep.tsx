'use client'

import { BottomBar } from '@/components/BottomBar'
import { HospitalizationForm } from '@/app/(private)/hospitalizations/(hospitalization_id)/components/HospitalizationForm'
import { HospitalizationFormData } from '@/validations/hospitalization'
import { useCreateHospitalization } from '@/hooks/mutations/hospitalizations'
import { Stack, Typography } from '@mui/material'
import { useSnackbar } from 'notistack'
import { useQueryClient } from '@tanstack/react-query'
import { buildHospitalizationPayload } from '../onboardingAdapters'

type HospitalizationStepProps = {
  teamId: string
  patientId: string
  onCompleted: (data: { place: string; sector: string }) => void
}

export const HospitalizationStep = ({ teamId, patientId, onCompleted }: HospitalizationStepProps) => {
  const queryClient = useQueryClient()
  const { enqueueSnackbar } = useSnackbar()
  const { mutateAsync: createHospitalization, isPending } = useCreateHospitalization()

  const submitAction = async (payload: HospitalizationFormData) => {
    createHospitalization({
      patient_id: patientId,
      payload: buildHospitalizationPayload(payload, teamId),
    })
      .then(() => {
        queryClient.invalidateQueries({ queryKey: ['hospitalizations'] })
        onCompleted({ place: payload.place, sector: payload.sector })
      })
      .catch(() => {
        enqueueSnackbar('Não foi possível cadastrar a internação.', { variant: 'error' })
      })
  }

  return (
    <Stack sx={{ minHeight: '100%', flex: 1 }}>
      <Stack className="p-4" gap={1}>
        <Typography variant="h6">Registrar internação</Typography>
        <Typography variant="body2" color="text.secondary">
          Cadastre a internação para o paciente criado na etapa anterior.
        </Typography>
      </Stack>
      <Stack className="p-4 pt-0">
        <HospitalizationForm
          submitAction={submitAction}
          isPending={isPending}
          initialData={{
            medical_team_id: teamId,
            number: '',
            place: '',
            sector: '',
            reason: '',
            observations: '',
          }}
        />
      </Stack>
      <BottomBar>
        <BottomBar.ActionContained type="submit" form={HospitalizationForm.id} loading={isPending}>
          Concluir onboarding
        </BottomBar.ActionContained>
      </BottomBar>
    </Stack>
  )
}
