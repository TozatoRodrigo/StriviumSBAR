'use client'

import { Box, Stack, TextField } from '@mui/material'
import { Controller, useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { TeamFormData, TeamSchema } from '@/validations/team'
import { useResetOnDataChange } from '@/hooks/useResetOnDataChange'

type TeamFormProps = {
  formId?: string
  initialData?: TeamFormData
  submitAction: (payload: TeamFormData) => void
  isPending: boolean
}

const defaultValues: TeamFormData = { name: '', description: '' }

const id = 'team-form'

export const TeamForm = ({ formId = id, submitAction, isPending, initialData = defaultValues }: TeamFormProps) => {
  const { handleSubmit, control, reset } = useForm<TeamFormData>({
    resolver: zodResolver(TeamSchema),
    defaultValues: initialData,
  })

  useResetOnDataChange(initialData, reset)

  return (
    <Stack id={formId} className="p-4" flex={1} gap={2} component="form" onSubmit={handleSubmit(submitAction)}>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <Controller
          name="name"
          control={control}
          render={({ field, fieldState }) => (
            <TextField
              label="Nome da equipe"
              variant="filled"
              {...field}
              error={!!fieldState.error}
              helperText={fieldState.error?.message}
              disabled={isPending}
            />
          )}
        />

        <Controller
          name="description"
          control={control}
          render={({ field, fieldState }) => (
            <TextField
              multiline
              rows={5}
              variant="filled"
              label="Descrição"
              {...field}
              error={!!fieldState.error}
              helperText={fieldState.error?.message}
              disabled={isPending}
            />
          )}
        />
      </Box>
    </Stack>
  )
}

TeamForm.id = id
