import { z } from 'zod/v4'

export const LoginSchema = z.object({
  login: z.string().min(1, 'Usuário obrigatório').max(100, 'Máximo de 100 caracteres'),
  password: z.string().min(1, 'Senha obrigatória').max(255),
  'cf-turnstile-response': z.string().optional(),
})

export type LoginFormData = z.infer<typeof LoginSchema>
