import { isValidCPF } from '@/lib/utils'
import { z } from 'zod/v4'

export const CpfSchema = z
  .string()
  .transform(value => value.replace(/[^\d]+/g, ''))
  .refine(isValidCPF, { message: 'CPF inválido' })
