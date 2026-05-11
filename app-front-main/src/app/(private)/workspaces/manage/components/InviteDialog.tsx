import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Button,
  FormControl,
  InputLabel,
  Select,
  FormHelperText,
} from '@mui/material'
import { Controller, useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { InviteFormData, WorkspaceInviteSchema } from '@/validations/workspace-invite'
import { useWorkspaceSendInvite } from '@/hooks/mutations/workspacesUser'
import { useMemo } from 'react'
import { useUserRoles } from '@/hooks/queries/roles'
import { useSnackbar } from 'notistack'
import { rolesOptions } from '@/constants/roles'
import { memberTypesOptions } from '@/constants/memberTypes'

type InviteDialogProps = {
  open: boolean
  onClose: () => void
}

export const InviteDialog = ({ open, onClose }: InviteDialogProps) => {
  const { enqueueSnackbar } = useSnackbar()
  const { data, isLoading: isLoadingRoles } = useUserRoles()
  const roles = useMemo(() => data?.data, [data?.data])

  const {
    register,
    handleSubmit,
    formState: { errors },
    control,
    watch,
    setValue,
  } = useForm<InviteFormData>({
    resolver: zodResolver(WorkspaceInviteSchema),
    defaultValues: {
      email: '',
      role_id: '',
      member_type: undefined,
      role_name: '',
    },
  })

  const selectedRoleId = watch('role_id')
  const selectedRole = useMemo(() => roles?.find(role => role.id === selectedRoleId), [roles, selectedRoleId])
  const isMemberRole = selectedRole?.name === 'member'

  const { mutateAsync, isPending } = useWorkspaceSendInvite()

  const handleInvite = ({ email, role_id, member_type }: InviteFormData) => {
    mutateAsync({ payload: { email, role_id, member_type } })
      .then(() => {
        enqueueSnackbar('Convite enviado com sucesso!', { variant: 'success' })
        onClose()
      })
      .catch(e => {
        // TODO: tratar error
        console.log(e)
        enqueueSnackbar('Não foi possível enviar o convite!', { variant: 'error' })
      })
  }

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      slotProps={{
        paper: {
          component: 'form',
          onSubmit: handleSubmit(handleInvite),
        },
      }}
    >
      <DialogTitle>Enviar Convite</DialogTitle>
      <DialogContent>
        <TextField
          label="Email"
          fullWidth
          margin="normal"
          {...register('email')}
          error={!!errors.email}
          helperText={errors.email?.message}
        />

        <Controller
          name="role_id"
          control={control}
          render={({ field, fieldState }) => (
            <FormControl error={!!fieldState.error} disabled={isPending || isLoadingRoles} fullWidth margin="normal">
              <InputLabel id="select-team">Permissão</InputLabel>
              <Select
                labelId="select-team"
                {...field}
                onChange={e => {
                  const roleId = e.target.value
                  field.onChange(roleId)
                  const role = roles?.find(r => r.id === roleId)
                  setValue('role_name', role?.name)
                  if (role?.name !== 'member') {
                    setValue('member_type', undefined)
                  }
                }}
                label="Permissão"
              >
                {roles?.map(({ id, name, description }) => (
                  <MenuItem key={id} value={id}>
                    {rolesOptions.find(role => role.id === name)?.label ?? ''} - {description}
                  </MenuItem>
                ))}
              </Select>
              {fieldState.error && <FormHelperText>{fieldState.error.message}</FormHelperText>}
            </FormControl>
          )}
        />
        {isMemberRole && (
          <Controller
            name="member_type"
            control={control}
            render={({ field, fieldState }) => (
              <FormControl error={!!fieldState.error} fullWidth margin="normal">
                <InputLabel id="select-member-type">Tipo</InputLabel>
                <Select labelId="select-member-type" {...field} value={field.value || ''} label="Tipo">
                  {memberTypesOptions?.map(({ id, name }) => (
                    <MenuItem key={id} value={id}>
                      {name}
                    </MenuItem>
                  ))}
                </Select>
                {fieldState.error && <FormHelperText>{fieldState.error.message}</FormHelperText>}
              </FormControl>
            )}
          />
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={isPending}>
          Cancelar
        </Button>
        <Button type="submit" variant="contained" disabled={isPending} loading={isPending}>
          Enviar
        </Button>
      </DialogActions>
    </Dialog>
  )
}
