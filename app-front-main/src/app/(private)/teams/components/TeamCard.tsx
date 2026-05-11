import { lazy, useState } from 'react'
import { MenuOptions } from '@/components/MenuOptions'
import { Button, Card, CardHeader, MenuItem, Skeleton } from '@mui/material'
import EditIcon from '@mui/icons-material/Edit'
import DeleteIcon from '@mui/icons-material/Delete'
import { useRouter } from 'next/navigation'
import { useDeleteTeam } from '@/hooks/mutations/teams'
import { useQueryClient } from '@tanstack/react-query'
import { useSnackbar } from 'notistack'

const AlertDialog = lazy(() => import('@/components/AlertDialog').then(module => ({ default: module.AlertDialog })))

type Team = {
  id: string
  name: string
  description: string
}

export const TeamCard = ({ id, name, description }: Team) => {
  const nav = useRouter()
  const queryClient = useQueryClient()
  const [modal, setModal] = useState({ id: 'none' })
  const { mutateAsync, isPending } = useDeleteTeam()
  const { anchorEl, handleClose, handleOpen } = MenuOptions.useMenuOptions()
  const { enqueueSnackbar } = useSnackbar()

  const handleDelete = () => {
    mutateAsync({ id }).then(() => {
      setModal({ id: 'none' })
      handleClose()
      enqueueSnackbar('Equipe excluida com sucesso!', { variant: 'success' })
      queryClient.invalidateQueries({ queryKey: ['teams'] })
    })
  }

  return (
    <>
      <Card>
        <CardHeader
          action={
            <MenuOptions anchorEl={anchorEl} onOpen={handleOpen} onClose={handleClose}>
              <MenuItem onClick={() => nav.push(`/teams/edit?team_id=${id}`)}>
                <EditIcon fontSize="small" sx={{ color: '#49454F' }} />
                <span className="ml-2">Editar</span>
              </MenuItem>
              <MenuItem
                onClick={() => {
                  setModal({ id: 'delete' })
                  handleClose()
                }}
              >
                <DeleteIcon fontSize="small" color="error" />
                <span className="ml-2 text-red-500">Excluir</span>
              </MenuItem>
            </MenuOptions>
          }
          title={name}
          subheader={description}
          slotProps={{ title: { fontSize: '0.875rem' }, subheader: { fontSize: '0.75rem' } }}
        />
      </Card>
      {modal.id === 'delete' && (
        <AlertDialog
          open={modal.id === 'delete'}
          actions={
            <>
              <Button onClick={() => setModal({ id: 'none' })} disabled={isPending}>
                Não
              </Button>
              <Button variant="contained" color="error" onClick={handleDelete} loading={isPending}>
                Excluir
              </Button>
            </>
          }
          title="Excluir equipe"
          content={`Deseja excluir a equipe ${name}?`}
          onClose={() => {}}
        />
      )}
    </>
  )
}

const TeamCardSkeleton = () => {
  return (
    <Card>
      <CardHeader
        action={<Skeleton variant="circular" width={32} height={32} />}
        title={<Skeleton variant="text" width="60%" height={20} />}
        subheader={<Skeleton variant="text" width="40%" height={16} />}
        slotProps={{
          title: { fontSize: '0.875rem' },
          subheader: { fontSize: '0.75rem' },
        }}
      />
    </Card>
  )
}

TeamCard.Skeleton = TeamCardSkeleton
