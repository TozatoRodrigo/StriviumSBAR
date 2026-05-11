'use client'

import { Box } from '@mui/material'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import { BottomBar } from '@/components/BottomBar'
import { TopBar } from '@/components/TopBar'
import Link from 'next/link'
import { useHospitalizationParams } from '@/hooks/queryParams/hospitalizations'
import { EvolutionForm } from './components/EvolutionForm'
import { useSnackbar } from 'notistack'
import { useCreateEvolution } from '@/hooks/mutations/evolutions'
import { useFromQuery } from '@/hooks/queryParams/from'

export default function Create() {
  const router = useRouter()
  const { hospitalization_id } = useHospitalizationParams()
  const { fromQuery } = useFromQuery()
  const { enqueueSnackbar } = useSnackbar()

  const { mutateAsync, isPending } = useCreateEvolution()

  const detailHref = `/hospitalizations/detail?hospitalization_id=${hospitalization_id}${
    fromQuery ? `&${fromQuery}` : ''
  }`

  const submitAction = async (payload: FormData) => {
    mutateAsync({ hospitalization_id: hospitalization_id!, payload })
      .then(() => {
        enqueueSnackbar('Evolução cadastrada com sucesso!', { variant: 'success' })
        router.push(detailHref)
      })
      .catch(e => {
        // TODO: tratar error
        console.log(e)
        enqueueSnackbar('Não foi possível cadastrar a evolução!', { variant: 'error' })
      })
  }

  useEffect(() => {
    if (!hospitalization_id) {
      enqueueSnackbar('Internação não localizada!', { variant: 'error' })
      router.push('/hospitalizations/pendings')
    }
  }, [enqueueSnackbar, hospitalization_id, router])

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
      <TopBar>
        <TopBar.Back disabled={isPending} href={detailHref} />
        <TopBar.Title>Registrar visita</TopBar.Title>
      </TopBar>
      <EvolutionForm submitAction={submitAction} isPending={isPending} />
      <BottomBar>
        <BottomBar.ActionOutlined LinkComponent={Link} href={detailHref} disabled={isPending}>
          Cancelar
        </BottomBar.ActionOutlined>
        <BottomBar.ActionContained type="submit" form={EvolutionForm.id} loading={isPending}>
          Salvar
        </BottomBar.ActionContained>
      </BottomBar>
    </Box>
  )
}
