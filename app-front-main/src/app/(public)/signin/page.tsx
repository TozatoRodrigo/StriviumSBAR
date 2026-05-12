'use client'

import { useEffect } from 'react'
import { Button, Divider, Fade, FilledInput, FormControl, FormHelperText, Stack, Typography } from '@mui/material'
import InputAdornment from '@mui/material/InputAdornment'
import AccountCircle from '@mui/icons-material/AccountCircle'
import Lock from '@mui/icons-material/Lock'
import Image from 'next/image'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { LoginFormData, LoginSchema } from '@/validations/login'
import { useAuth } from '@/contexts/AuthContext'
import Link from 'next/link'
import { InputPassword } from '@/components/InputPassword'
import { Turnstile } from '@/components/Turnstile'

const Signin = () => {
  const {
    login,
    states: { isAuthenticating },
  } = useAuth()
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(LoginSchema),
  })

  useEffect(() => {
    register('cf-turnstile-response')
  }, [register])

  const onSubmit = ({ login: _login, password, ...rest }: LoginFormData) => {
    login({ payload: { login: _login, password }, headers: { 'x-turnstile-token': rest['cf-turnstile-response'] } })
  }

  return (
    <Fade in appear>
      <Stack gap={2} pt={4}>
        <Image
          className="self-center"
          src="/logo.svg"
          alt="Strivium logo"
          unoptimized
          width={67.82}
          height={80}
          priority
          fetchPriority="high"
        />
        <Stack alignItems="center">
          <Typography component="h1" className="font-bold text-[#020617] text-xl">
            Acesse sua conta
          </Typography>
          <Typography variant="subtitle2" className="font-normal text-[#64748B]">
            Comunicação eficiente para cuidar melhor!
          </Typography>
        </Stack>

        <form onSubmit={handleSubmit(onSubmit)} className="grid gap-6">
          <Stack gap={2}>
            <FormControl>
              <FilledInput
                type="text"
                {...register('login')}
                autoFocus
                autoComplete="username"
                placeholder="E-mail ou CRM"
                error={!!errors.login}
                slotProps={{
                  input: {
                    sx: {
                      '&.MuiFilledInput-input': {
                        padding: '1rem',
                      },
                    },
                  },
                }}
                startAdornment={
                  <InputAdornment position="start">
                    <AccountCircle />
                  </InputAdornment>
                }
              />
              {!!errors.login && <FormHelperText error>{errors.login.message}</FormHelperText>}
            </FormControl>

            <FormControl>
              <InputPassword
                {...register('password')}
                startAdornment={
                  <InputAdornment position="start">
                    <Lock />
                  </InputAdornment>
                }
              />
              {!!errors.password && <FormHelperText error>{errors.password.message}</FormHelperText>}
            </FormControl>

            <Turnstile onSuccess={token => setValue('cf-turnstile-response', token)} />
          </Stack>

          <Stack gap={2}>
            <Button type="submit" variant="contained" className="rounded-full" loading={isAuthenticating}>
              Acessar
            </Button>
            <Button
              type="button"
              LinkComponent={Link}
              href="/recovery-password"
              variant="text"
              disabled={isAuthenticating}
              hidden /* TODO[v1]: enable */
            >
              Esqueci minha senha
            </Button>
            <Divider>
              <Typography sx={{ alignSelf: 'center' }} className="font-semibold text-[#020617]">
                ou
              </Typography>
            </Divider>
            <Button LinkComponent={Link} href="/signup" variant="text" disabled={isAuthenticating}>
              Criar conta
            </Button>
          </Stack>
        </form>
      </Stack>
    </Fade>
  )
}

export default Signin
