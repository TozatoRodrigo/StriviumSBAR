import { genders } from '@/constants/common'
import { medicalSpecialties } from '@/constants/specialties'
import { brazilianStates } from '@/constants/states'
import { z } from 'zod/v4'
import { CpfSchema } from './schemas/cpf'
import { CellphoneSchema } from './schemas/cellphone'
import { BirthDateSchema } from './schemas/birthDate'

export const DoctorSchema = z.object({
  full_name: z
    .string({
      error: issue => (issue.input === undefined ? 'Nome é obrigatório' : 'Nome inválido'),
    })
    .min(5, 'Nome deve ter pelo menos 5 caracteres')
    .trim(),
  birth_date: BirthDateSchema,
  gender: z.enum(
    genders.map(({ value }) => value),
    'Selecione um gênero'
  ),
  document: CpfSchema,
  cellphone: CellphoneSchema,
  email: z.email('Informe um e-mail válido'),
  specialty: z.enum(
    Object.keys(medicalSpecialties) as [keyof typeof medicalSpecialties],
    'Selecione uma especialidade'
  ),
  crm_uf: z.enum(
    brazilianStates.map(({ acronym }) => acronym),
    'Selecione um UF'
  ),
  crm_number: z.string().trim().min(1, 'CRM é obrigatório').max(7, 'CRM deve ter no máximo 7 caracteres'),
})

export type DoctorFormData = z.infer<typeof DoctorSchema>
