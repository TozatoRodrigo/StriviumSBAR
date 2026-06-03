'use client'

import { BottomBar } from '@/components/BottomBar'
import { useCreateTeam } from '@/hooks/mutations/teams'
import { TeamFormData } from '@/validations/team'
import { TeamForm } from '@/app/(private)/teams/components/TeamForm'
import { Stack, Typography } from '@mui/material'
import { useSnackbar } from 'notistack'
import { useQueryClient } from '@tanstack/react-query'

type TeamStepProps = {
  onCompleted: (data: { teamId: string; teamName: string }) => void
}

export const TeamStep = ({ onCompleted }: TeamStepProps) => {
  const queryClient = useQueryClient()
  const { enqueueSnackbar } = useSnackbar()
  const { mutateAsync: createTeam, isPending } = useCreateTeam()

  const submitAction = async (payload: TeamFormData) => {
    createTeam({ payload })
      .then(team => {
        queryClient.invalidateQueries({ queryKey: ['teams'] })
        onCompleted({ teamId: team.id, teamName: team.name })
      })
      .catch(() => {
        enqueueSnackbar('Não foi possível criar a equipe.', { variant: 'error' })
      })
  }

  return (
    <Stack sx={{ minHeight: '100%', flex: 1 }}>
      <Stack className="p-4" gap={1}>
        <Typography variant="h6">Sua equipe médica</Typography>
        <Typography variant="body2" color="text.secondary">
          Crie a equipe que vai atender os pacientes internados.
        </Typography>
      </Stack>
      <TeamForm submitAction={submitAction} isPending={isPending} />
      <BottomBar>
        <BottomBar.ActionContained type="submit" form={TeamForm.id} loading={isPending}>
          Continuar
        </BottomBar.ActionContained>
      </BottomBar>
    </Stack>
  )
}
