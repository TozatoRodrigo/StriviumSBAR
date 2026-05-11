'use client'

import { TopBar } from '@/components/TopBar'
import { HOSPITALIZATIONS } from '@/routes'
import { Box } from '@mui/material'
import { HospitalizationForm } from '../components/HospitalizationForm'
import { BottomBar } from '@/components/BottomBar'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useUpdateHospitalization } from '@/hooks/mutations/hospitalizations'
import { useSnackbar } from 'notistack'
import { useHospitalizationParams } from '@/hooks/queryParams/hospitalizations'
import { useEffect, useMemo } from 'react'
import { useHospitalization } from '@/hooks/queries/hospitalizations'
import { HospitalizationFormData, HospitalizationSchema } from '@/validations/hospitalization'
import { useCallbackParams } from '@/hooks/queryParams/utils'
import { Content } from '@/components/Content'

export default function Edit() {
  const router = useRouter()
  const { mutateAsync, isPending } = useUpdateHospitalization()
  const { enqueueSnackbar } = useSnackbar()
  const { callbackUrl } = useCallbackParams()

  const { hospitalization_id } = useHospitalizationParams()
  const { data, isLoading } = useHospitalization(hospitalization_id!, { enabled: !!hospitalization_id })
  // TODO: o tipo do data foi alterado, corrigir o schema
  // TODO: tratar esse parse, ele pode estourar erro
  const initialData = useMemo<HospitalizationFormData | undefined>(
    () => (data ? HospitalizationSchema.parse(data) : undefined),
    [data]
  )

  const submitAction = async (payload: HospitalizationFormData) => {
    if (!data) return
    mutateAsync({ id: hospitalization_id!, patient_id: data.patient_id, payload })
      .then(() => {
        enqueueSnackbar('Internação atualizada com sucesso!', { variant: 'success' })

        return callbackUrl ? router.push(callbackUrl) : router.back()
      })
      .catch(e => {
        // TODO: tratar error
        console.log(e)
        enqueueSnackbar('Não foi possível atualizar a internação!', { variant: 'error' })
      })
  }

  useEffect(() => {
    if (!hospitalization_id) {
      enqueueSnackbar('Internação não localizada!', { variant: 'error' })
      router.push('/hospitalizations/pendings')
    }
  }, [hospitalization_id, enqueueSnackbar, router])

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
      <TopBar>
        <TopBar.Back href={callbackUrl ?? HOSPITALIZATIONS.PENDINGS} />
        <TopBar.Title>Editar internação</TopBar.Title>
      </TopBar>
      <Content>
        <HospitalizationForm submitAction={submitAction} isPending={isPending || isLoading} initialData={initialData} />
      </Content>
      <BottomBar>
        <BottomBar.ActionOutlined
          LinkComponent={Link}
          href={callbackUrl ?? HOSPITALIZATIONS.PENDINGS}
          disabled={isPending}
        >
          Voltar
        </BottomBar.ActionOutlined>
        <BottomBar.ActionContained type="submit" form={HospitalizationForm.id} loading={isPending}>
          Salvar
        </BottomBar.ActionContained>
      </BottomBar>
    </Box>
  )
}
