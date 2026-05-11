'use client'

import { Box, Stack, Typography } from '@mui/material'
import { BottomBar } from '@/components/BottomBar'
import { TopBar } from '@/components/TopBar'
import { HOSPITALIZATIONS } from '@/routes'
import { useCallbackParams, useFormStepsParams } from '@/hooks/queryParams/utils'
import { PatientForm } from '../components/PatientForm'
import Link from 'next/link'
import { enqueueSnackbar } from 'notistack'
import { useRouter } from 'next/navigation'
import { PatientPayload, useCreatePatient } from '@/hooks/mutations/patients'
import { PatientFormData } from '@/validations/patient'
import { splitFullname } from '@/lib/utils'

export default function Create() {
  const { callbackUrl } = useCallbackParams()
  const { current_step, steps, withFormSteps } = useFormStepsParams()
  const router = useRouter()

  const { mutateAsync, isPending } = useCreatePatient()

  const submitAction = async (payload: PatientFormData) => {
    const formatted: PatientPayload = {
      ...payload,
      first_name: splitFullname(payload.full_name).name,
      last_name: splitFullname(payload.full_name).surname,
      birth_date: payload.birth_date.toISOString().substring(0, 10),
      document_number: null,
    }

    mutateAsync({ payload: formatted })
      .then(({ id }) => {
        enqueueSnackbar('Paciente cadastrado com sucesso!', { variant: 'success' })
        const callback = callbackUrl + `?patient_id=${id}`

        return callbackUrl ? router.push(callback) : router.back()
      })
      .catch(e => {
        // TODO: tratar error
        console.log(e)
        enqueueSnackbar('Não foi possível cadastrar o paciente!', { variant: 'error' })
      })
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
      <TopBar>
        {/* TODO: pegar o link da pagina que chamou */}
        <TopBar.Back href={HOSPITALIZATIONS.PENDINGS} />
        <TopBar.Title>Cadastrar paciente</TopBar.Title>
      </TopBar>

      <Stack className="p-4" flex={1} gap={2}>
        {withFormSteps && (
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
              {current_step}
            </Box>
            <Box>
              <Typography variant="caption" fontWeight="medium" color="text.secondary">
                Passo {current_step} de {steps}
              </Typography>
              <Typography variant="body1" fontWeight="normal">
                Dados pessoais
              </Typography>
            </Box>
          </Stack>
        )}
        <PatientForm submitAction={submitAction} isPending={isPending} />
      </Stack>

      <BottomBar>
        {/* TODO: pegar o link da pagina que chamou */}
        <BottomBar.ActionOutlined LinkComponent={Link} href={HOSPITALIZATIONS.PENDINGS} disabled={isPending}>
          Voltar
        </BottomBar.ActionOutlined>
        <BottomBar.ActionContained type="submit" form={PatientForm.id} loading={isPending}>
          Salvar
        </BottomBar.ActionContained>
      </BottomBar>
    </Box>
  )
}
