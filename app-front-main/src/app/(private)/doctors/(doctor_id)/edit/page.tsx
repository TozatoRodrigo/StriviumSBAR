'use client'

import { TopBar } from '@/components/TopBar'
import { HOSPITALIZATIONS } from '@/routes'
import { Box } from '@mui/material'
import { DoctorForm } from '../../components/DoctorForm'
import { BottomBar } from '@/components/BottomBar'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { DoctorPayload, useUpdateDoctor } from '@/hooks/mutations/doctors'
import { useSnackbar } from 'notistack'
import { useDoctorParams } from '@/hooks/queryParams/doctors'
import { useEffect, useMemo } from 'react'
import { useDoctor } from '@/hooks/queries/doctors'
import { DoctorFormData, DoctorSchema } from '@/validations/doctor'

export default function Edit() {
  const router = useRouter()
  const { mutateAsync, isPending } = useUpdateDoctor()
  const { enqueueSnackbar } = useSnackbar()

  const { doctor_id } = useDoctorParams()
  const { data, isLoading } = useDoctor(String(doctor_id), { enabled: !!doctor_id })

  // TODO: tratar esse parse, ele pode estourar erro
  const initialData = useMemo<DoctorFormData | undefined>(() => (data ? DoctorSchema.parse(data) : undefined), [data])

  const submitAction = async (payload: DoctorFormData) => {
    const formatted: DoctorPayload = {
      ...payload,
      birth_date: payload.birth_date.toISOString().substring(0, 10),
    }

    mutateAsync({ id: String(doctor_id), payload: formatted })
      .then(() => {
        enqueueSnackbar('Médico atualizado com sucesso!', { variant: 'success' })

        router.back()
      })
      .catch(e => {
        // TODO: tratar error
        console.log(e)
        enqueueSnackbar('Não foi possível atualizar o médico!', { variant: 'error' })
      })
  }

  useEffect(() => {
    if (!doctor_id) {
      enqueueSnackbar('Médico não localizado!', { variant: 'error' })
      router.push('/hospitalizations/pendings')
    }
  }, [doctor_id, enqueueSnackbar, router])

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
      <TopBar>
        <TopBar.Back href={HOSPITALIZATIONS.PENDINGS} />
        <TopBar.Title>Editar médico</TopBar.Title>
      </TopBar>

      <DoctorForm submitAction={submitAction} isPending={isPending || isLoading} initialData={initialData} />

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
