'use client'

import { Alert, Button, Chip, Stack, TextField, Typography } from '@mui/material'
import { useMemo, useState } from 'react'
import { useSnackbar } from 'notistack'

import { BottomBar } from '@/components/BottomBar'
import { useAuth } from '@/contexts/AuthContext'
import { MemberType } from '@/constants/memberTypes'
import { useWorkspaceSendInvite } from '@/hooks/mutations/workspacesUser'
import { useUserRoles } from '@/hooks/queries/roles'
import { buildDoctorInvitePayload, findDoctorRoleId } from '../onboardingAdapters'

type InviteStepProps = {
  onCompleted: (data: { inviteCount: number }) => void
}

const isValidEmail = (value: string) => /\S+@\S+\.\S+/.test(value)

export const InviteStep = ({ onCompleted }: InviteStepProps) => {
  const { enqueueSnackbar } = useSnackbar()
  const [email, setEmail] = useState('')
  const [invitedEmails, setInvitedEmails] = useState<string[]>([])

  const {
    info: authInfo,
  } = useAuth()
  const { data, isLoading: isLoadingRoles, isError: isRolesError } = useUserRoles()
  const { mutateAsync: sendInvite, isPending: isSendingInvite } = useWorkspaceSendInvite()

  const doctorRoleId = useMemo(() => findDoctorRoleId(data?.data), [data?.data])

  const handleInvite = async () => {
    const normalizedEmail = email.trim().toLowerCase()

    if (!isValidEmail(normalizedEmail)) {
      enqueueSnackbar('Informe um email válido.', { variant: 'error' })
      return
    }

    if (authInfo?.email === normalizedEmail) {
      enqueueSnackbar('Você não pode convidar o próprio usuário.', { variant: 'error' })
      return
    }

    if (invitedEmails.includes(normalizedEmail)) {
      enqueueSnackbar('Este email já foi convidado nesta etapa.', { variant: 'warning' })
      return
    }

    if (!doctorRoleId) {
      enqueueSnackbar('Não foi possível carregar o papel de médico.', { variant: 'error' })
      return
    }

    sendInvite({ payload: buildDoctorInvitePayload(normalizedEmail, doctorRoleId) })
      .then(() => {
        setInvitedEmails(current => [...current, normalizedEmail])
        setEmail('')
      })
      .catch(() => {
        enqueueSnackbar('Não foi possível enviar o convite.', { variant: 'error' })
      })
  }

  const canSendInvite = !isLoadingRoles && !isSendingInvite && !!doctorRoleId

  return (
    <Stack sx={{ minHeight: '100%', flex: 1 }}>
      <Stack className="p-4" gap={2}>
        <Stack gap={1}>
          <Typography variant="h6">Convide sua equipe</Typography>
          <Typography variant="body2" color="text.secondary">
            Esta etapa é opcional. Você pode pular e convidar depois.
          </Typography>
        </Stack>

        <Alert severity="info">Os convites serão enviados com o papel de {MemberType.DOCTOR}.</Alert>

        {isRolesError && (
          <Alert severity="warning">Não foi possível carregar permissões agora. Você pode pular esta etapa.</Alert>
        )}

        <Stack direction="row" gap={1}>
          <TextField
            label="Email do médico"
            type="email"
            variant="filled"
            value={email}
            onChange={event => setEmail(event.target.value)}
            disabled={isSendingInvite}
            fullWidth
          />
          <Button variant="outlined" onClick={handleInvite} disabled={!canSendInvite}>
            Adicionar
          </Button>
        </Stack>

        {!!invitedEmails.length && (
          <Stack direction="row" flexWrap="wrap" gap={1}>
            {invitedEmails.map(item => (
              <Chip key={item} label={item} color="success" variant="outlined" />
            ))}
          </Stack>
        )}
      </Stack>
      <BottomBar>
        <BottomBar.ActionOutlined onClick={() => onCompleted({ inviteCount: 0 })}>Pular</BottomBar.ActionOutlined>
        <BottomBar.ActionContained onClick={() => onCompleted({ inviteCount: invitedEmails.length })}>
          Continuar
        </BottomBar.ActionContained>
      </BottomBar>
    </Stack>
  )
}
