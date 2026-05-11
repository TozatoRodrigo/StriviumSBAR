import { z } from 'zod/v4'
import { BirthDateSchema } from './schemas/birthDate'

export const PatientSchema = z.object({
  full_name: z
    .string({
      error: issue => (issue.input === undefined ? 'Nome é obrigatório' : 'Nome inválido'),
    })
    .min(5, 'O nome completo deve ter pelo menos 5 caracteres')
    .trim(),
  birth_date: BirthDateSchema,
})

export type PatientFormData = z.infer<typeof PatientSchema>
