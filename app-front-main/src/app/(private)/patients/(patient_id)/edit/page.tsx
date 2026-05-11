'use client'

import { TopBar } from '@/components/TopBar'
import { HOSPITALIZATIONS } from '@/routes'
import { Box } from '@mui/material'
import { PatientForm } from '../../components/PatientForm'
import { BottomBar } from '@/components/BottomBar'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { PatientPayload, useUpdatePatient } from '@/hooks/mutations/patients'
import { useSnackbar } from 'notistack'
import { usePatientParams } from '@/hooks/queryParams/patients'
import { useEffect, useMemo } from 'react'
import { usePatientById } from '@/hooks/queries/patients'
import { PatientFormData, PatientSchema } from '@/validations/patient'
import { joinFullname, splitFullname } from '@/lib/utils'

export default function Edit() {
  const router = useRouter()
  const { mutateAsync, isPending } = useUpdatePatient()
  const { enqueueSnackbar } = useSnackbar()

  const { patient_id } = usePatientParams()
  const { data, isLoading } = usePatientById(patient_id!, { enabled: !!patient_id })

  // TODO: tratar esse parse, ele pode estourar erro
  const initialData = useMemo<PatientFormData | undefined>(
    () =>
      data ? PatientSchema.parse({ ...data, full_name: joinFullname(data.first_name, data.last_name) }) : undefined,
    [data]
  )

  const submitAction = async (payload: PatientFormData) => {
    const formatted: PatientPayload = {
      first_name: splitFullname(payload.full_name).name,
      last_name: splitFullname(payload.full_name).surname,
      birth_date: payload.birth_date.toISOString().substring(0, 10),
      document_number: null,
    }

    mutateAsync({ id: patient_id!, payload: formatted })
      .then(() => {
        enqueueSnackbar('Paciente atualizado com sucesso!', { variant: 'success' })

        router.back()
      })
      .catch(e => {
        // TODO: tratar error
        console.log(e)
        enqueueSnackbar('Não foi possível atualizar o paciente!', { variant: 'error' })
      })
  }

  useEffect(() => {
    if (!patient_id) {
      enqueueSnackbar('Paciente não localizado!', { variant: 'error' })
      router.push('/hospitalizations/pendings')
    }
  }, [patient_id, enqueueSnackbar, router])

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
      <TopBar>
        <TopBar.Back href={HOSPITALIZATIONS.PENDINGS} />
        <TopBar.Title>Editar paciente</TopBar.Title>
      </TopBar>

      <PatientForm submitAction={submitAction} isPending={isPending || isLoading} initialData={initialData} />

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
