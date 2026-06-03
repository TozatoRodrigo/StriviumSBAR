'use client'

import { BottomBar } from '@/components/BottomBar'
import { useCreatePatient } from '@/hooks/mutations/patients'
import { PatientFormData } from '@/validations/patient'
import { PatientForm } from '@/app/(private)/patients/components/PatientForm'
import { Stack, Typography } from '@mui/material'
import { useSnackbar } from 'notistack'
import { useQueryClient } from '@tanstack/react-query'
import { buildPatientPayload } from '../onboardingAdapters'

type PatientStepProps = {
  onCompleted: (data: { patientId: string; patientName: string }) => void
}

export const PatientStep = ({ onCompleted }: PatientStepProps) => {
  const queryClient = useQueryClient()
  const { enqueueSnackbar } = useSnackbar()
  const { mutateAsync: createPatient, isPending } = useCreatePatient()

  const submitAction = async (payload: PatientFormData) => {
    createPatient({ payload: buildPatientPayload(payload) })
      .then(patient => {
        queryClient.invalidateQueries({ queryKey: ['patients'] })
        onCompleted({ patientId: patient.id, patientName: payload.full_name })
      })
      .catch(() => {
        enqueueSnackbar('Não foi possível cadastrar o paciente.', { variant: 'error' })
      })
  }

  return (
    <Stack sx={{ minHeight: '100%', flex: 1 }}>
      <Stack className="p-4" gap={1}>
        <Typography variant="h6">Cadastre o primeiro paciente</Typography>
        <Typography variant="body2" color="text.secondary">
          Informe os dados do paciente que será internado.
        </Typography>
      </Stack>
      <PatientForm submitAction={submitAction} isPending={isPending} />
      <BottomBar>
        <BottomBar.ActionContained type="submit" form={PatientForm.id} loading={isPending}>
          Continuar
        </BottomBar.ActionContained>
      </BottomBar>
    </Stack>
  )
}
