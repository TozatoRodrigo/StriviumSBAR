'use client'

import { Divider, FormHelperText, Stack, Typography } from '@mui/material'
import { z } from 'zod/v4'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { ptBR } from 'date-fns/locale/pt-BR'
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'

import { Box, FormControl, InputLabel, MenuItem, Select, TextField } from '@mui/material'
import { Controller } from 'react-hook-form'
import { DatePicker } from '@mui/x-date-pickers/DatePicker'
import { brazilianStates } from '@/constants/states'
import { medicalSpecialties } from '@/constants/specialties'
import { CpfMaskInput } from '@/components/CpfMarkInput'
import { PhoneMaskInput } from '@/components/PhoneMaskInput'
import { DoctorFormData, DoctorSchema } from '@/validations/doctor'
import { genders } from '@/constants/common'
import { useResetOnDataChange } from '@/hooks/useResetOnDataChange'

type DoctorFormProps = {
  formId?: string
  initialData?: DoctorFormData
  isPending: boolean
  submitAction: (payload: DoctorFormData) => void
}

const id = 'team-form'

const defaultValues: DoctorFormData = {
  full_name: '',
  email: '',
  document: '',
  crm_number: '',
  cellphone: '',
  crm_uf: '' as 'PR',
  gender: '' as 'male',
  specialty: '' as 'ACUPUNCTURE',
  birth_date: null as unknown as Date,
}

export const DoctorForm = ({ formId = id, submitAction, isPending, initialData = defaultValues }: DoctorFormProps) => {
  const {
    handleSubmit,
    control,
    reset,
    formState: { errors },
  } = useForm<z.input<typeof DoctorSchema>, object, z.output<typeof DoctorSchema>>({
    resolver: zodResolver(DoctorSchema),
    defaultValues: initialData,
  })

  useResetOnDataChange(initialData, reset)

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ptBR}>
      <Stack id={formId} className="p-4" flex={1} gap={2} component="form" onSubmit={handleSubmit(submitAction)}>
        <Typography fontSize={16} fontWeight={500}>
          Dados pessoais
        </Typography>
        <Divider />
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Controller
            name="full_name"
            control={control}
            render={({ field, fieldState }) => (
              <TextField
                label="Nome completo"
                variant="filled"
                {...field}
                error={!!fieldState.error}
                helperText={fieldState.error?.message}
                disabled={isPending}
              />
            )}
          />
          <Controller
            name="birth_date"
            control={control}
            render={({ field }) => (
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
                    error: !!errors.birth_date,
                    helperText: errors.birth_date?.message,
                  },
                }}
              />
            )}
          />
          <Controller
            name="gender"
            control={control}
            render={({ field }) => (
              <FormControl variant="filled" error={!!errors.gender} disabled={isPending}>
                <InputLabel id="select-gender">Gênero</InputLabel>
                <Select labelId="select-gender" {...field} label="Selecione o gênero" variant="filled">
                  {genders.map(({ value, label }) => (
                    <MenuItem key={value} value={value}>
                      {label}
                    </MenuItem>
                  ))}
                </Select>
                {errors.gender && <FormHelperText>{errors.gender.message}</FormHelperText>}
              </FormControl>
            )}
          />
          <Controller
            name="document"
            control={control}
            render={({ field, fieldState }) => (
              <TextField
                label="CPF"
                variant="filled"
                {...field}
                error={!!fieldState.error}
                helperText={fieldState.error?.message}
                disabled={isPending}
                slotProps={{
                  input: { inputComponent: CpfMaskInput },
                }}
              />
            )}
          />

          <Controller
            name="cellphone"
            control={control}
            render={({ field, fieldState }) => (
              <TextField
                label="Celular"
                variant="filled"
                {...field}
                error={!!fieldState.error}
                helperText={fieldState.error?.message}
                disabled={isPending}
                slotProps={{
                  input: { inputComponent: PhoneMaskInput },
                }}
              />
            )}
          />
          <Controller
            name="email"
            control={control}
            render={({ field, fieldState }) => (
              <TextField
                label="E-mail"
                variant="filled"
                {...field}
                error={!!fieldState.error}
                helperText={fieldState.error?.message}
                disabled={isPending}
              />
            )}
          />
        </Box>
        <Typography fontSize={16} fontWeight={500} mt={2}>
          Dados profissionais
        </Typography>
        <Divider />
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Stack direction="row" gap={2}>
            <Controller
              name="crm_uf"
              control={control}
              render={({ field }) => (
                <FormControl variant="filled" error={!!errors.crm_uf} disabled={isPending} className="min-w-[150px]">
                  <InputLabel id="select-crm_uf">Estado do CRM</InputLabel>
                  <Select labelId="select-crm_uf" {...field} label="Selecione o estado" variant="filled">
                    {brazilianStates?.map(({ acronym }) => (
                      <MenuItem key={acronym} value={acronym}>
                        {acronym}
                      </MenuItem>
                    ))}
                  </Select>
                  {errors.crm_uf && <FormHelperText>{errors.crm_uf.message}</FormHelperText>}
                </FormControl>
              )}
            />
            <Controller
              name="crm_number"
              control={control}
              render={({ field, fieldState }) => (
                <TextField
                  label="CRM"
                  fullWidth
                  variant="filled"
                  {...field}
                  error={!!fieldState.error}
                  helperText={fieldState.error?.message}
                  disabled={isPending}
                />
              )}
            />
          </Stack>

          <Controller
            name="specialty"
            control={control}
            render={({ field }) => (
              <FormControl variant="filled" error={!!errors.specialty} disabled={isPending}>
                <InputLabel id="select-specialty">Especialidade</InputLabel>
                <Select labelId="select-specialty" {...field} label="Selecione a especialidade" variant="filled">
                  {Object.entries(medicalSpecialties).map(([key, value]) => (
                    <MenuItem key={key} value={key}>
                      {value}
                    </MenuItem>
                  ))}
                </Select>
                {errors.specialty && <FormHelperText>{errors.specialty.message}</FormHelperText>}
              </FormControl>
            )}
          />
        </Box>
      </Stack>
    </LocalizationProvider>
  )
}

DoctorForm.id = id
