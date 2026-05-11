import { MenuOptions } from '@/components/MenuOptions'
import { Button, Card, CardContent, CardHeader, MenuItem, Skeleton, Typography } from '@mui/material'
import EditIcon from '@mui/icons-material/Edit'
import DeleteIcon from '@mui/icons-material/Delete'
import { usePathname, useRouter } from 'next/navigation'
import { joinFullname, withCallbackRoute } from '@/lib/utils'
import { format } from '@/lib/date'
import { useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { useDeleteHospitalization } from '@/hooks/mutations/hospitalizations'
import { useSnackbar } from 'notistack'
import { AlertDialog } from '@/components/AlertDialog'

type Hospitalization = {
  id: string
  patient: {
    first_name: string
    last_name: string
  }
  created_at: string
  sector: string
  reason: string
  place: string
  status: string
}

export const HospitalizationCard = ({ id, patient, created_at, sector, reason, place }: Hospitalization) => {
  const nav = useRouter()
  const queryClient = useQueryClient()
  const pathname = usePathname()
  const [modal, setModal] = useState({ id: 'none' })
  const { mutateAsync, isPending } = useDeleteHospitalization()
  const { anchorEl, handleClose, handleOpen } = MenuOptions.useMenuOptions()
  const name = joinFullname(patient.first_name, patient.last_name)

  const { enqueueSnackbar } = useSnackbar()

  const handleDelete = () => {
    mutateAsync({ id }).then(() => {
      setModal({ id: 'none' })
      handleClose()
      enqueueSnackbar('Internação excluida com sucesso!', { variant: 'success' })
      queryClient.invalidateQueries({ queryKey: ['hospitalizations'] })
    })
  }

  return (
    <>
      <Card>
        <CardHeader
          action={
            <MenuOptions anchorEl={anchorEl} onOpen={handleOpen} onClose={handleClose}>
              <MenuItem
                onClick={() => nav.push(withCallbackRoute(`/hospitalizations/edit?hospitalization_id=${id}`, pathname))}
              >
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
          subheader={format(created_at, 'dd/MM/yyyy')}
          slotProps={{ title: { fontSize: '0.875rem' }, subheader: { fontSize: '0.75rem' } }}
        />
        <CardContent>
          <Typography>Setor: {sector}</Typography>
          <Typography>Motivo: {reason}</Typography>
          <Typography>Local: {place}</Typography>
        </CardContent>
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
          title="Excluir internação"
          content={`Deseja excluir a internação de(a) ${name}?`}
          onClose={() => {}}
        />
      )}
    </>
  )
}

const HospitalizationCardSkeleton = () => {
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
      <CardContent>
        <Skeleton variant="text" width="40%" height={20} />
        <Skeleton variant="text" width="40%" height={20} />
        <Skeleton variant="text" width="40%" height={20} />
      </CardContent>
    </Card>
  )
}

HospitalizationCard.Skeleton = HospitalizationCardSkeleton
