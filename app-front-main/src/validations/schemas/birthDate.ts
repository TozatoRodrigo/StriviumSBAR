import { isAfter, isValid } from 'date-fns'
import { z } from 'zod/v4'

const today = new Date()

export const BirthDateSchema = z
  .preprocess(val => {
    if (val === null || val === undefined || val === '') return undefined

    if (typeof val === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(val)) {
      const [year, month, day] = val.split('-').map(Number)
      return new Date(year, month - 1, day)
    }
    return val
  }, z.coerce.date())
  .refine(val => val instanceof Date && isValid(val), {
    message: 'Data inválida',
  })
  .refine(val => !isAfter(val, today), {
    message: 'A data não pode estar no futuro',
  })
