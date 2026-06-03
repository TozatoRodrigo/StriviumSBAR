import Stack from '@mui/material/Stack'
import TextField from '@mui/material/TextField'
import { Controller, useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { WorkspaceFormData, WorkspaceSchema } from '@/validations/workspace'
import { z } from 'zod/v4'
import { useResetOnDataChange } from '@/hooks/useResetOnDataChange'

type WorkspaceFormProps = {
  formId?: string
  initialData?: WorkspaceFormData
  submitAction: (payload: WorkspaceFormData) => void
  isPending: boolean
}

const id = 'workspace-form'

const defaultValues: WorkspaceFormData = {
  name: '',
}

export const WorkspaceForm = ({
  formId = id,
  submitAction,
  isPending,
  initialData = defaultValues,
}: WorkspaceFormProps) => {
  const { handleSubmit, control, reset } = useForm<
    z.input<typeof WorkspaceSchema>,
    object,
    z.output<typeof WorkspaceSchema>
  >({
    resolver: zodResolver(WorkspaceSchema),
    defaultValues: initialData,
  })

  useResetOnDataChange(initialData, reset)

  return (
    <Stack id={formId} className="p-4" flex={1} gap={2} component="form" onSubmit={handleSubmit(submitAction)}>
      <Controller
        name="name"
        control={control}
        render={({ field, fieldState }) => (
          <TextField
            label="Nome do local"
            variant="filled"
            {...field}
            disabled={isPending}
            error={!!fieldState.error}
            helperText={fieldState.error?.message}
          />
        )}
      />
    </Stack>
  )
}

WorkspaceForm.id = id
