'use client'

import { Box, Stack, Typography } from '@mui/material'
import { HospitalizationForm } from '../../(hospitalization_id)/components/HospitalizationForm'
import { useCreateHospitalization } from '@/hooks/mutations/hospitalizations'
import { useSnackbar } from 'notistack'
import { useRouter } from 'next/navigation'
import { HospitalizationFormData } from '@/validations/hospitalization'

type HospitalizationStepProps = {
  selectedId: string
}

export function HospitalizationStep({ selectedId }: HospitalizationStepProps) {
  const router = useRouter()
  const { enqueueSnackbar } = useSnackbar()
  const { mutateAsync, isPending } = useCreateHospitalization()

  const submitAction = (data: HospitalizationFormData) => {
    mutateAsync({ patient_id: selectedId, payload: data })
      .then(() => {
        enqueueSnackbar('Internação cadastrada com sucesso!', { variant: 'success' })
        router.push('/')
      })
      .catch(e => {
        // TODO: tratar error
        console.log(e)
        enqueueSnackbar('Não foi possível cadastrar a internação!', { variant: 'error' })
      })
  }

  return (
    <Stack gap={2}>
      <Stack direction="row" alignItems="center" spacing={1}>
        <Box
          sx={{
            width: 28,
            height: 28,
            bgcolor: '#4283F1',
            borderRadius: '50%',
            color: 'white',
            fontSize: 14,
            fontWeight: 'bold',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          2
        </Box>
        <Box>
          <Typography variant="caption" fontWeight="medium" color="text.secondary">
            Passo 2 de 2
          </Typography>
          <Typography variant="body1" fontWeight="normal">
            Internação
          </Typography>
        </Box>
      </Stack>

      <HospitalizationForm submitAction={submitAction} isPending={isPending} />
    </Stack>
  )
}
