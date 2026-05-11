import { z } from 'zod/v4'

export const CellphoneSchema = z
  .string()
  .nonempty('Informe um telefone')
  .transform(val => val.replace(/\D/g, ''))
  .refine(val => /^(\d{10}|\d{11})$/.test(val), {
    message: 'Telefone inválido',
  })
