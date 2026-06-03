'use client'

import { useCreateWorkspace, useSigninWorkspaceMutation } from '@/hooks/mutations/workspaces'
import { WorkspaceFormData } from '@/validations/workspace'
import { BottomBar } from '@/components/BottomBar'
import { WorkspaceForm } from '@/app/(private)/workspaces/components/WorkspaceForm'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import { useSnackbar } from 'notistack'
import { useWorkspaceToken } from '@/contexts/WorkspaceTokenContext'
import { useQueryClient } from '@tanstack/react-query'

type WorkspaceStepProps = {
  onCompleted: (data: { tenantId: string; workspaceName: string }) => void
}

export const WorkspaceStep = ({ onCompleted }: WorkspaceStepProps) => {
  const queryClient = useQueryClient()
  const { enqueueSnackbar } = useSnackbar()
  const { addTokens } = useWorkspaceToken()
  const { mutateAsync: createWorkspace, isPending: isCreatingWorkspace } = useCreateWorkspace()
  const { mutateAsync: signinWorkspace, isPending: isSigningWorkspace } = useSigninWorkspaceMutation()

  const submitAction = async (payload: WorkspaceFormData) => {
    createWorkspace({ payload })
      .then(workspace =>
        signinWorkspace({ tenant_id: workspace.id }).then(tokens => ({
          workspace,
          access_token: tokens.access_token,
          refresh_token: tokens.refresh_token,
        }))
      )
      .then(({ workspace, access_token, refresh_token }) => {
        addTokens({ access: access_token, refresh: refresh_token })
        queryClient.invalidateQueries({ queryKey: ['workspaces'] })
        onCompleted({ tenantId: workspace.id, workspaceName: workspace.name })
      })
      .catch(() => {
        enqueueSnackbar('Não foi possível criar o local de trabalho.', { variant: 'error' })
      })
  }

  const isPending = isCreatingWorkspace || isSigningWorkspace

  return (
    <Stack sx={{ minHeight: '100%', flex: 1 }}>
      <Stack className="p-4" gap={1}>
        <Typography variant="h6">Seu local de trabalho</Typography>
        <Typography variant="body2" color="text.secondary">
          Cadastre o hospital, clínica ou consultório onde você atende.
        </Typography>
      </Stack>
      <WorkspaceForm submitAction={submitAction} isPending={isPending} />
      <BottomBar>
        <BottomBar.ActionContained type="submit" form={WorkspaceForm.id} loading={isPending}>
          Continuar
        </BottomBar.ActionContained>
      </BottomBar>
    </Stack>
  )
}
