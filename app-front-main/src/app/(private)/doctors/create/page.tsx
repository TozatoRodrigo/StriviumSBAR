'use client'

import { TopBar } from '@/components/TopBar'
import { HOSPITALIZATIONS } from '@/routes'
import { Box } from '@mui/material'
import { DoctorForm } from '../components/DoctorForm'
import { BottomBar } from '@/components/BottomBar'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { DoctorPayload, useCreateDoctor } from '@/hooks/mutations/doctors'
import { useSnackbar } from 'notistack'
import { DoctorFormData } from '@/validations/doctor'

export default function Create() {
  const router = useRouter()
  const { mutateAsync, isPending } = useCreateDoctor()
  const { enqueueSnackbar } = useSnackbar()

  const submitAction = async (payload: DoctorFormData) => {
    const formatted: DoctorPayload = {
      ...payload,
      birth_date: payload.birth_date.toISOString().substring(0, 10),
    }

    mutateAsync({ payload: formatted })
      .then(() => {
        enqueueSnackbar('Médico cadastrado com sucesso!', { variant: 'success' })

        router.back()
      })
      .catch(e => {
        // TODO: tratar error
        console.log(e)
        enqueueSnackbar('Não foi possível cadastrar o médico!', { variant: 'error' })
      })
  }
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
      <TopBar>
        <TopBar.Back href={HOSPITALIZATIONS.PENDINGS} />
        <TopBar.Title>Cadastrar médico</TopBar.Title>
      </TopBar>
      <DoctorForm submitAction={submitAction} isPending={isPending} />

      <BottomBar>
        {/* TODO: pegar o link da pagina que chamou */}
        <BottomBar.ActionOutlined LinkComponent={Link} href={HOSPITALIZATIONS.PENDINGS} disabled={isPending}>
          Voltar
        </BottomBar.ActionOutlined>
        <BottomBar.ActionContained type="submit" form={DoctorForm.id} loading={isPending}>
          Salvar
        </BottomBar.ActionContained>
      </BottomBar>
    </Box>
  )
}
