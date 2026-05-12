'use client'

import { useEffect } from 'react'
import { Fade, FormControl, FormHelperText, Stack, TextField, Typography } from '@mui/material'
import Image from 'next/image'

import { Controller, useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { AccountFormData, AccountFormDataInput, AccountFormDataOutput, AccountSchema } from '@/validations/account'
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers'
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'
import { CpfMaskInput } from '@/components/CpfMarkInput'
import { InputPassword } from '@/components/InputPassword'
import { SignupPayload, useSignupMutation } from '@/hooks/mutations/account'
import { useRouter } from 'next/navigation'
import { useSnackbar } from 'notistack'
import { BottomBar } from '@/components/BottomBar'
import Link from 'next/link'
import { Turnstile } from '@/components/Turnstile'

export default function Signup() {
  const { handleSubmit, control, setValue } = useForm<AccountFormDataInput, object, AccountFormDataOutput>({
    resolver: zodResolver(AccountSchema),
    defaultValues: {
      birth_date: null as unknown as Date,
      confirm_password: '',
      document: '',
      email: '',
      first_name: '',
      last_name: '',
      password: '',
    },
  })

  useEffect(() => {
    control.register('cf-turnstile-response')
  }, [control])

  const { mutateAsync, isPending } = useSignupMutation()
  const nav = useRouter()
  const { enqueueSnackbar } = useSnackbar()

  const submit = (payload: AccountFormData) => {
    const formatted: SignupPayload = {
      ...payload,
      birth_date: payload.birth_date.toISOString().substring(0, 10),
    }

    mutateAsync({ payload: formatted, headers: { 'x-turnstile-token': payload['cf-turnstile-response'] } })
      .then(() => enqueueSnackbar('Usuário cadastrado com sucesso!', { variant: 'success' }))
      .then(() => nav.push('/'))
      .catch(e => enqueueSnackbar(e.message))
  }

  return (
    <Fade in appear>
      <Stack gap={2} pt={4}>
        <Image className="self-center" src="/logo.svg" alt="Strivium logo" unoptimized width={67.82} height={80} />
        <Stack alignItems="center">
          <Typography component="h1" className="font-bold text-[#020617] text-xl">
            Cadastrar sua conta
          </Typography>
          <Typography variant="subtitle2" className="font-normal text-[#64748B]">
            Comunicação eficiente para cuidar melhor!
          </Typography>
        </Stack>

        <LocalizationProvider dateAdapter={AdapterDateFns}>
          <Stack className="p-4" flex={1} gap={2} component="form" onSubmit={handleSubmit(submit)}>
            <Controller
              name="first_name"
              control={control}
              render={({ field, fieldState }) => (
                <TextField
                  label="Primeiro Nome"
                  variant="filled"
                  {...field}
                  error={!!fieldState.error}
                  helperText={fieldState.error?.message}
                  disabled={isPending}
                />
              )}
            />
            <Controller
              name="last_name"
              control={control}
              render={({ field, fieldState }) => (
                <TextField
                  label="Sobrenome"
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
              name="email"
              control={control}
              render={({ field, fieldState }) => (
                <TextField
                  label="Email"
                  variant="filled"
                  {...field}
                  error={!!fieldState.error}
                  helperText={fieldState.error?.message}
                />
              )}
            />

            <Controller
              name="password"
              control={control}
              render={({ field, fieldState }) => (
                <FormControl>
                  <InputPassword {...field} error={!!fieldState.error} disabled={isPending} />
                  {!!fieldState.error && <FormHelperText error>{fieldState.error.message}</FormHelperText>}
                </FormControl>
              )}
            />
            <Controller
              name="confirm_password"
              control={control}
              render={({ field, fieldState }) => (
                <TextField
                  label="Confirmar Senha"
                  type="password"
                  variant="filled"
                  {...field}
                  error={!!fieldState.error}
                  helperText={fieldState.error?.message}
                  disabled={isPending}
                />
              )}
            />
            {/* TODO: adicionar o campo de uf do crm. Ao habilitar, se o crm for informado, o uf é obrigatório */}
            {/* <Controller
              name="crm"
              control={control}
              render={({ field, fieldState }) => (
                <TextField
                  label="CRM (opcional)"
                  variant="filled"
                  {...field}
                  error={!!fieldState.error}
                  helperText={fieldState.error?.message}
                  disabled={false}
                />
              )}
            /> */}

            <Turnstile onSuccess={token => setValue('cf-turnstile-response', token)} />

            <BottomBar>
              <BottomBar.ActionOutlined LinkComponent={Link} color="error" href={`/signin`} disabled={isPending}>
                Cancelar
              </BottomBar.ActionOutlined>
              <BottomBar.ActionContained type="submit" loading={isPending}>
                Criar Conta
              </BottomBar.ActionContained>
            </BottomBar>
          </Stack>
        </LocalizationProvider>
      </Stack>
    </Fade>
  )
}
