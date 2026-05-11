'use client'

import { BottomBar } from '@/components/BottomBar'
import { TopBar } from '@/components/TopBar'
import { HOSPITALIZATIONS } from '@/routes'
import { Box } from '@mui/material'
import Link from 'next/link'
import { TeamForm } from '../components/TeamForm'
import { useRouter } from 'next/navigation'
import { useSnackbar } from 'notistack'
import { useCreateTeam } from '@/hooks/mutations/teams'
import { TeamFormData } from '@/validations/team'

export default function Create() {
  const router = useRouter()
  const { enqueueSnackbar } = useSnackbar()

  const { mutateAsync, isPending } = useCreateTeam()

  const submitAction = async (payload: TeamFormData) => {
    mutateAsync({ payload })
      .then(() => {
        enqueueSnackbar('Equipe cadastrada com sucesso!', { variant: 'success' })
        router.push(`/hospitalizations/pendings`)
      })
      .catch(e => {
        // TODO: tratar error
        console.log(e)
        enqueueSnackbar('Não foi possível cadastrar a equipe!', { variant: 'error' })
      })
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
      <TopBar>
        <TopBar.Back href={HOSPITALIZATIONS.PENDINGS} />
        <TopBar.Title>Cadastrar equipe</TopBar.Title>
      </TopBar>
      <TeamForm submitAction={submitAction} isPending={isPending} />
      <BottomBar>
        <BottomBar.ActionOutlined LinkComponent={Link} href={`/hospitalizations/pendings`} disabled={isPending}>
          Cancelar
        </BottomBar.ActionOutlined>
        <BottomBar.ActionContained type="submit" form={TeamForm.id} loading={isPending}>
          Salvar
        </BottomBar.ActionContained>
      </BottomBar>
    </Box>
  )
}
