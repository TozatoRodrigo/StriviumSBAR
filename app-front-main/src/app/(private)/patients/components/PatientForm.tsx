import { Stack, TextField } from '@mui/material'
import { Controller, useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { DatePicker } from '@mui/x-date-pickers/DatePicker'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'
import { ptBR } from 'date-fns/locale/pt-BR'
import { PatientFormData, PatientSchema } from '@/validations/patient'
import { z } from 'zod/v4'
import { useResetOnDataChange } from '@/hooks/useResetOnDataChange'

type PatientFormProps = {
  formId?: string
  initialData?: PatientFormData
  submitAction: (payload: PatientFormData) => void
  isPending: boolean
}

const id = 'patient-form'

const defaultValues: PatientFormData = {
  full_name: '',
  birth_date: null as unknown as Date,
}

export const PatientForm = ({
  formId = id,
  submitAction,
  isPending,
  initialData = defaultValues,
}: PatientFormProps) => {
  const { handleSubmit, control, reset } = useForm<
    z.input<typeof PatientSchema>,
    object,
    z.output<typeof PatientSchema>
  >({
    resolver: zodResolver(PatientSchema),
    defaultValues: initialData,
  })

  useResetOnDataChange(initialData, reset)

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ptBR}>
      <Stack id={formId} className="p-4" flex={1} gap={2} component="form" onSubmit={handleSubmit(submitAction)}>
        <Controller
          name="full_name"
          control={control}
          render={({ field, fieldState }) => (
            <TextField
              label="Nome completo"
              variant="filled"
              {...field}
              disabled={isPending}
              error={!!fieldState.error}
              helperText={fieldState.error?.message}
            />
          )}
        />

        <Controller
          name="birth_date"
          control={control}
          render={({ field, fieldState }) => (
            <DatePicker
              label="Data de nascimento"
              value={field.value as Date}
              format="dd/MM/yyyy"
              disableFuture
              disabled={isPending}
              onChange={date => {
                field.onChange(date ?? undefined)
              }}
              slotProps={{
                textField: {
                  variant: 'filled',
                  error: !!fieldState.error,
                  helperText: fieldState.error?.message,
                },
              }}
            />
          )}
        />
      </Stack>
    </LocalizationProvider>
  )
}

PatientForm.id = id
