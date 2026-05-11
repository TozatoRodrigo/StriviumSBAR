'use client'

import { BottomBar } from '@/components/BottomBar'
import { TopBar } from '@/components/TopBar'
import { HOSPITALIZATIONS } from '@/routes'
import { Box } from '@mui/material'
import Link from 'next/link'
import { WorkspaceForm } from '../components/WorkspaceForm'
import { useRouter } from 'next/navigation'
import { useSnackbar } from 'notistack'
import { WorkspaceFormData } from '@/validations/workspace'
import { useCreateWorkspace } from '@/hooks/mutations/workspaces'

export default function Create() {
  const router = useRouter()
  const { enqueueSnackbar } = useSnackbar()
  const { mutateAsync, isPending } = useCreateWorkspace()

  const submitAction = async (payload: WorkspaceFormData) => {
    mutateAsync({ payload })
      .then(() => {
        enqueueSnackbar('Local de trabalho cadastrado com sucesso!', { variant: 'success' })
        router.push('/workspaces')
      })
      .catch(e => {
        // TODO: tratar error
        console.log(e)
        enqueueSnackbar('Não foi possível cadastrar o local de trabalho!', { variant: 'error' })
      })
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
      <TopBar>
        <TopBar.Back href={HOSPITALIZATIONS.PENDINGS} />
        <TopBar.Title>Cadastrar local de trabalho</TopBar.Title>
      </TopBar>
      <WorkspaceForm submitAction={submitAction} isPending={isPending} />
      <BottomBar>
        <BottomBar.ActionOutlined LinkComponent={Link} href="/workspaces" disabled={isPending}>
          Cancelar
        </BottomBar.ActionOutlined>
        <BottomBar.ActionContained type="submit" form={WorkspaceForm.id} loading={isPending}>
          Salvar
        </BottomBar.ActionContained>
      </BottomBar>
    </Box>
  )
}
