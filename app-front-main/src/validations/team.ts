import { z } from 'zod/v4'

export const TeamSchema = z.object({
  name: z
    .string({
      error: issue => (issue.input === undefined ? 'Nome é obrigatório' : 'Nome inválido'),
    })
    .min(5, 'Nome deve ter pelo menos 5 caracteres')
    .trim(),
  description: z
    .string()
    .trim()
    .transform(val => val ?? ''),
})

export type TeamFormData = z.infer<typeof TeamSchema>
