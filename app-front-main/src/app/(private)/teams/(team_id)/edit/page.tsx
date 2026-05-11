'use client'

import { TopBar } from '@/components/TopBar'
import { HOSPITALIZATIONS } from '@/routes'
import { Box } from '@mui/material'
import { TeamForm } from '../../components/TeamForm'
import { BottomBar } from '@/components/BottomBar'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useUpdateTeam } from '@/hooks/mutations/teams'
import { useSnackbar } from 'notistack'
import { useTeamParams } from '@/hooks/queryParams/teams'
import { useEffect, useMemo } from 'react'
import { useTeam } from '@/hooks/queries/teams'
import { TeamFormData, TeamSchema } from '@/validations/team'

export default function Edit() {
  const router = useRouter()
  const { mutateAsync, isPending } = useUpdateTeam()
  const { enqueueSnackbar } = useSnackbar()

  const { team_id } = useTeamParams()
  const { data, isLoading } = useTeam(team_id!, { enabled: !!team_id })

  // TODO: tratar esse parse, ele pode estourar erro
  const initialData = useMemo<TeamFormData | undefined>(() => (data ? TeamSchema.parse(data) : undefined), [data])

  const submitAction = async (payload: TeamFormData) => {
    mutateAsync({ id: team_id!, payload })
      .then(() => {
        enqueueSnackbar('Equipe atualizada com sucesso!', { variant: 'success' })

        router.back()
      })
      .catch(e => {
        // TODO: tratar error
        console.log(e)
        enqueueSnackbar('Não foi possível atualizar a equipe!', { variant: 'error' })
      })
  }

  useEffect(() => {
    if (!team_id) {
      enqueueSnackbar('Equipe não localizada!', { variant: 'error' })
      router.push('/hospitalizations/pendings')
    }
  }, [team_id, enqueueSnackbar, router])

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
      <TopBar>
        <TopBar.Back href={HOSPITALIZATIONS.PENDINGS} />
        <TopBar.Title>Editar equipe</TopBar.Title>
      </TopBar>

      <TeamForm submitAction={submitAction} isPending={isPending || isLoading} initialData={initialData} />

      <BottomBar>
        {/* TODO: pegar o link da pagina que chamou */}
        <BottomBar.ActionOutlined LinkComponent={Link} href={HOSPITALIZATIONS.PENDINGS} disabled={isPending}>
          Voltar
        </BottomBar.ActionOutlined>
        <BottomBar.ActionContained type="submit" form={TeamForm.id} loading={isPending}>
          Salvar
        </BottomBar.ActionContained>
      </BottomBar>
    </Box>
  )
}
