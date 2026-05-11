import { z } from 'zod/v4'
import { CpfSchema } from './schemas/cpf'
import { BirthDateSchema } from './schemas/birthDate'

export const AccountSchema = z
  .object({
    first_name: z
      .string()
      .min(3, 'O primeiro nome deve ter no mínimo 3 caracteres')
      .max(150, 'O primeiro nome deve ter no máximo 150 caracteres')
      .describe('Primeiro nome do usuário'),

    last_name: z
      .string()
      .min(3, 'O sobrenome deve ter no mínimo 3 caracteres')
      .max(150, 'O sobrenome deve ter no máximo 150 caracteres')
      .describe('Sobrenome do usuário'),

    /* crm: z
      .string()
      .trim()
      .min(1, 'O CRM deve ter no mínimo 1 caracter')
      .max(7, 'O CRM deve ter no máximo 50 caracteres')
      .nullable()
      .optional()
      .describe('Número do CRM do médico'), */

    document: CpfSchema.nullable().optional().describe('CPF do usuário (apenas números)'),

    email: z.email('Email inválido').describe('Email do usuário'),

    password: z
      .string()
      .min(6, 'A senha deve ter no mínimo 6 caracteres')
      .describe('Senha do usuário (mínimo 6 caracteres)'),

    confirm_password: z.string().min(6, 'A senha deve ter no mínimo 6 caracteres'),

    birth_date: BirthDateSchema,

    'cf-turnstile-response': z.string().optional(),
  })
  .refine(data => data.password === data.confirm_password, {
    path: ['confirm_password'],
    message: 'As senhas não coincidem',
  })

export type AccountFormData = z.infer<typeof AccountSchema>
export type AccountFormDataInput = z.input<typeof AccountSchema>
export type AccountFormDataOutput = z.output<typeof AccountSchema>
