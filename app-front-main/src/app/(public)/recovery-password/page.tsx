'use client'

import { Fade, Stack, TextField, Typography } from '@mui/material'
import Image from 'next/image'

import { Controller, useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { LocalizationProvider } from '@mui/x-date-pickers'
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'
import { BottomBar } from '@/components/BottomBar'
import Link from 'next/link'
import { z } from 'zod/v4'

export default function RecoveryPassword() {
  const { handleSubmit, control } = useForm({
    resolver: zodResolver(z.object({ email: z.email('E-mail inválido') })),
    defaultValues: {
      email: '',
    },
  })

  const isPending = false
  // TODO: implementar
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const submit = (_payload: unknown) => {}

  return (
    <Fade in appear>
      <Stack gap={2} pt={4}>
        <Image className="self-center" src="/logo.svg" alt="Strivium logo" unoptimized width={67.82} height={80} />
        <Stack alignItems="center">
          <Typography component="h1" className="font-bold text-[#020617] text-xl">
            Recuperar conta
          </Typography>
          <Typography variant="subtitle2" className="font-normal text-[#64748B]">
            Comunicação eficiente para cuidar melhor!
          </Typography>
        </Stack>

        <LocalizationProvider dateAdapter={AdapterDateFns}>
          <Stack className="p-4" flex={1} gap={2} component="form" onSubmit={handleSubmit(submit)}>
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

            <BottomBar>
              <BottomBar.ActionOutlined LinkComponent={Link} color="error" href={`/signin`} disabled={isPending}>
                Cancelar
              </BottomBar.ActionOutlined>
              <BottomBar.ActionContained type="submit" loading={isPending}>
                Recuperar Conta
              </BottomBar.ActionContained>
            </BottomBar>
          </Stack>
        </LocalizationProvider>
      </Stack>
    </Fade>
  )
}
