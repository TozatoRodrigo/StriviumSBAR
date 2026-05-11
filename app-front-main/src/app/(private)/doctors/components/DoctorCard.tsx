import { MenuOptions } from '@/components/MenuOptions'
import { Button, Card, CardHeader, MenuItem, Skeleton } from '@mui/material'
import EditIcon from '@mui/icons-material/Edit'
import DeleteIcon from '@mui/icons-material/Delete'
import { useRouter } from 'next/navigation'
import { joinFullname } from '@/lib/utils'
import { AlertDialog } from '@/components/AlertDialog'
import { useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { useDeleteDoctor } from '@/hooks/mutations/doctors'
import { useSnackbar } from 'notistack'

type Doctor = {
  id: string
  first_name: string
  last_name: string
  crm: {
    number: number
    uf: string
  }
}

export const DoctorCard = ({ id, first_name, last_name, crm }: Doctor) => {
  const nav = useRouter()
  const queryClient = useQueryClient()
  const [modal, setModal] = useState({ id: 'none' })
  const { mutateAsync, isPending } = useDeleteDoctor()
  const { anchorEl, handleClose, handleOpen } = MenuOptions.useMenuOptions()
  const name = joinFullname(first_name, last_name)
  const crmLabel = `${crm.number}/${crm.uf}`

  const { enqueueSnackbar } = useSnackbar()

  const handleDelete = () => {
    mutateAsync({ id }).then(() => {
      setModal({ id: 'none' })
      handleClose()
      enqueueSnackbar('Médico excluido com sucesso!', { variant: 'success' })
      queryClient.invalidateQueries({ queryKey: ['doctors'] })
    })
  }

  return (
    <>
      <Card>
        <CardHeader
          action={
            <MenuOptions anchorEl={anchorEl} onOpen={handleOpen} onClose={handleClose}>
              <MenuItem onClick={() => nav.push(`/doctors/edit?doctor_id=${id}`)}>
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
          subheader={crmLabel}
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
          title="Excluir médico"
          content={`Deseja excluir o(a) médico(a) ${name}?`}
          onClose={() => {}}
        />
      )}
    </>
  )
}

const DoctorCardSkeleton = () => {
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

DoctorCard.Skeleton = DoctorCardSkeleton
