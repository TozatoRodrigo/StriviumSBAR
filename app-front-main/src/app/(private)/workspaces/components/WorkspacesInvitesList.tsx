import { Button, Card, CardActions, Stack, Typography } from '@mui/material'
import { WorkspaceCard } from './WorkspaceCard'
import { useMemo, useState } from 'react'
import { ErrorState } from '@/components/ErrorState'
import { useWorkspacesPendingInvites } from '@/hooks/queries/workspacesUser'
import BusinessCenterOutlinedIcon from '@mui/icons-material/BusinessCenterOutlined'
import { WorkspacesInvitesEmptyList } from './WorkspacesInvitesEmptyList'
import { useWorkspaceAcceptInvite, useWorkspaceDeclineInvite } from '@/hooks/mutations/workspacesUser'
import { useSnackbar } from 'notistack'
import { AlertDialog } from '@/components/AlertDialog'
import { useQueryClient } from '@tanstack/react-query'

type Modal =
  | {
      id: 'none'
      props?: never
    }
  | {
      id: 'decline'
      props: { id: string; tenant: { id: string; name: string } }
    }

export const WorkspacesInvitesList = () => {
  const { data, isLoading, isError, refetch } = useWorkspacesPendingInvites()

  const invites = useMemo(() => data?.data, [data?.data])
  const { enqueueSnackbar } = useSnackbar()
  const { mutateAsync: declineInvite, isPending } = useWorkspaceDeclineInvite()
  const { mutateAsync: acceptInvite } = useWorkspaceAcceptInvite()
  const queryClient = useQueryClient()
  const [modal, setModal] = useState<Modal>({ id: 'none' })

  if (isLoading) return <WorkspacesInvitesListSkeleton />
  if (isError || !invites) return <ErrorState onRetry={refetch} />
  if (!invites.length) return <WorkspacesInvitesEmptyList />

  const onAccept = (id: string) => {
    acceptInvite({ id })
      .then(() => {
        refetch()
        queryClient.invalidateQueries({ queryKey: ['workspaces-invites-count'] })
      })
      .catch(() =>
        enqueueSnackbar('Ocorreu um erro ao aceitar o convite. Tente novamente mais tarde!', { variant: 'error' })
      )
  }

  const onDecline = ({ id, tenant }: { id: string; tenant: { id: string; name: string } }) => {
    setModal({ id: 'decline', props: { id, tenant } })
  }

  const handleDecline = (id: string) => {
    declineInvite({ id })
      .then(() => {
        setModal({ id: 'none' })
        refetch()
      })
      .catch(() =>
        enqueueSnackbar('Ocorreu um erro ao recusar o convite. Tente novamente mais tarde!', { variant: 'error' })
      )
  }

  return (
    <>
      <Stack className="p-4" flex={1} gap={2}>
        {invites.map(({ id, tenant }) => (
          // TODO: componentizar
          <Card key={id}>
            <Stack p={2} direction="row" justifyContent="space-between" alignItems="center" gap={2}>
              <BusinessCenterOutlinedIcon sx={{ color: '#64748B' }} />
              <Stack flex="1" className="font-normal text-sm ">
                {/* TODO: remover o  ? depois que o campo name for adicionado na api */}
                <Typography className="text-[#020617]">{tenant?.name}</Typography>
              </Stack>
            </Stack>
            <CardActions sx={{ justifyContent: 'end' }}>
              <Button size="small" color="error" onClick={() => onDecline({ id, tenant })}>
                Recusar
              </Button>
              <Button size="small" color="primary" onClick={() => onAccept(id)}>
                Aceitar
              </Button>
            </CardActions>
          </Card>
        ))}
      </Stack>
      {modal.id === 'decline' && (
        <AlertDialog
          open={modal.id === 'decline'}
          actions={
            <>
              <Button onClick={() => setModal({ id: 'none' })} disabled={isPending}>
                Não
              </Button>
              <Button
                variant="contained"
                color="error"
                onClick={() => handleDecline(modal.props.id)}
                loading={isPending}
              >
                Recusar
              </Button>
            </>
          }
          title="Recusar convite"
          content={`Deseja recusar o convite para ${modal.props.tenant?.name}?`}
          onClose={() => setModal({ id: 'none' })}
        />
      )}
    </>
  )
}

export const WorkspacesInvitesListSkeleton = () => {
  const placeholders = Array.from({ length: 3 })

  return (
    <Stack className="p-4" flex={1} gap={2}>
      {placeholders.map((_, index) => (
        <WorkspaceCard.Skeleton key={index} />
      ))}
    </Stack>
  )
}

WorkspacesInvitesList.Skeleton = WorkspacesInvitesListSkeleton
