import { Box, FormControl, FormHelperText, InputLabel, MenuItem, Select, TextField } from '@mui/material'
import { useForm, Controller } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useTeams } from '@/hooks/queries/teams'
import { HospitalizationFormData, HospitalizationSchema } from '@/validations/hospitalization'
import { useResetOnDataChange } from '@/hooks/useResetOnDataChange'
import { z } from 'zod/v4'
import { useMemo } from 'react'

type HospitalizationFormProps = {
  formId?: string
  initialData?: HospitalizationFormData
  submitAction: (payload: HospitalizationFormData) => void
  isPending: boolean
}

const id = 'hospitalization-form'

const defaultValues: HospitalizationFormData = {
  medical_team_id: '',
  number: '',
  place: '',
  sector: '',
  reason: '',
  observations: '',
}

export const HospitalizationForm = ({
  formId = id,
  submitAction,
  isPending,
  initialData = defaultValues,
}: HospitalizationFormProps) => {
  const { data, isLoading: isLoadingTeams } = useTeams({ params: { limit: 100 }, options: { enabled: true } })

  const teams = useMemo(() => data?.pages.flatMap(page => page.data), [data?.pages])

  const { handleSubmit, control, reset } = useForm<
    z.input<typeof HospitalizationSchema>,
    object,
    z.output<typeof HospitalizationSchema>
  >({
    resolver: zodResolver(HospitalizationSchema),
    defaultValues: initialData,
  })

  useResetOnDataChange(initialData, reset)

  return (
    <form id={formId} onSubmit={handleSubmit(submitAction)} noValidate>
      <Box display="flex" flexDirection="column" gap={2}>
        <Controller
          name="medical_team_id"
          control={control}
          render={({ field, fieldState }) => (
            <FormControl variant="filled" error={!!fieldState.error} disabled={isPending || isLoadingTeams}>
              <InputLabel id="select-team">Selecione a equipe</InputLabel>
              <Select labelId="select-team" {...field} label="Selecione a equipe" variant="filled">
                {teams?.map(({ id, name }) => (
                  <MenuItem key={id} value={id}>
                    {name}
                  </MenuItem>
                ))}
              </Select>
              {fieldState.error && <FormHelperText>{fieldState.error.message}</FormHelperText>}
            </FormControl>
          )}
        />

        <Controller
          name="number"
          control={control}
          render={({ field, fieldState }) => (
            <TextField
              {...field}
              label="Número de Internação (NI)"
              variant="filled"
              error={!!fieldState.error}
              helperText={fieldState.error?.message}
              disabled={isPending}
            />
          )}
        />

        <Controller
          name="place"
          control={control}
          render={({ field, fieldState }) => (
            <TextField
              {...field}
              label="Local da internação"
              variant="filled"
              error={!!fieldState.error}
              helperText={fieldState.error?.message}
              disabled={isPending}
            />
          )}
        />

        <Controller
          name="sector"
          control={control}
          render={({ field, fieldState }) => (
            <TextField
              {...field}
              label="Setor"
              variant="filled"
              error={!!fieldState.error}
              helperText={fieldState.error?.message}
              disabled={isPending}
            />
          )}
        />

        <Controller
          name="reason"
          control={control}
          render={({ field, fieldState }) => (
            <TextField
              {...field}
              label="Motivo da internação"
              variant="filled"
              multiline
              error={!!fieldState.error}
              helperText={fieldState.error?.message}
              disabled={isPending}
            />
          )}
        />

        <Controller
          name="observations"
          control={control}
          render={({ field, fieldState }) => (
            <TextField
              {...field}
              label="Observações (opcional)"
              variant="filled"
              multiline
              error={!!fieldState.error}
              helperText={fieldState.error?.message}
              disabled={isPending}
            />
          )}
        />
      </Box>
    </form>
  )
}

HospitalizationForm.id = id
