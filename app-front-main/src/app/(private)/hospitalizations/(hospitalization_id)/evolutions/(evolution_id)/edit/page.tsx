'use client'

import { useRouter } from 'next/navigation'

import { useFromQuery } from '@/hooks/queryParams/from'
import { useHospitalizationParams } from '@/hooks/queryParams/hospitalizations'
import { Box } from '@mui/material'
import { TopBar } from '@/components/TopBar'
import { EvolutionForm } from '../../create/components/EvolutionForm'
import { BottomBar } from '@/components/BottomBar'
import Link from 'next/link'
import { useUpdateEvolution } from '@/hooks/mutations/evolutions'
import { useEvolution } from '@/hooks/queries/evolutions'
import { useSnackbar } from 'notistack'
import { useEvolutionParams } from '@/hooks/queryParams/evolution'
import { useEffect } from 'react'
import { useWorkspace } from '@/contexts/WorkspaceContext'
import { useAuth } from '@/contexts/AuthContext'

export default function Edit() {
  const router = useRouter()
  const { evolution_id } = useEvolutionParams()
  const { hospitalization_id } = useHospitalizationParams()
  const { enqueueSnackbar } = useSnackbar()
  const {
    states: { isRole },
  } = useWorkspace()

  const { info } = useAuth()

  const { fromQuery } = useFromQuery()
  const detailHref = `/hospitalizations/detail?hospitalization_id=${hospitalization_id}${
    fromQuery ? `&${fromQuery}` : ''
  }`
  const { data: evolution, isLoading: isLoadingEvolution } = useEvolution(hospitalization_id!, evolution_id!, {
    enabled: !!evolution_id,
  })

  const { mutateAsync, isPending } = useUpdateEvolution()

  const submitAction = async (payload: FormData) => {
    mutateAsync({ hospitalization_id: hospitalization_id!, payload, id: evolution_id! })
      .then(() => {
        enqueueSnackbar('Evolução atualizada com sucesso!', { variant: 'success' })
        router.push(detailHref)
      })
      .catch(e => {
        // TODO: tratar error
        console.log(e)
        enqueueSnackbar('Não foi possível atualizar a evolução!', { variant: 'error' })
      })
  }

  useEffect(() => {
    if (!isRole.admin && evolution?.user_id !== info?.id) {
      enqueueSnackbar('Você não tem permissão para editar essa evolução!', { variant: 'warning' })
      router.push(detailHref)
    }
  }, [detailHref, enqueueSnackbar, evolution?.user_id, info?.id, isRole.admin, router])

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
      <TopBar>
        <TopBar.Back disabled={isPending} href={detailHref} />
        <TopBar.Title>Editar visita</TopBar.Title>
      </TopBar>
      {evolution && (
        <EvolutionForm
          submitAction={submitAction}
          isPending={isPending || isLoadingEvolution}
          initialData={evolution}
        />
      )}
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
