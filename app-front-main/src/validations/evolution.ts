import { z } from 'zod/v4'
import { clinicalCourseOptions, priorityOptions, typeOptions } from '@/constants/evolutions'

const optionalText = z.string().trim().optional()

// TODO: validar os arquivos - https://dev.to/drprime01/how-to-validate-a-file-input-with-zod-5739
export const EvolutionSchema = z.object({
  type: z.enum(
    typeOptions.map(({ id }) => id),
    { error: 'Selecione uma opção' }
  ),
  situation: z
    .string({
      error: issue => (issue.input === undefined ? 'Situação é obrigatória' : 'Situação inválida'),
    })
    .trim()
    .min(5, 'Situação deve ter pelo menos 5 caracteres'),
  background: optionalText,
  assessment: z
    .string({
      error: issue => (issue.input === undefined ? 'Avaliação é obrigatória' : 'Avaliação inválida'),
    })
    .trim()
    .min(5, 'Avaliação deve ter pelo menos 5 caracteres'),
  recommendation: z
    .string({
      error: issue => (issue.input === undefined ? 'Plano é obrigatório' : 'Plano inválido'),
    })
    .trim()
    .min(5, 'Plano deve ter pelo menos 5 caracteres'),
  priority: z.enum(
    priorityOptions.map(({ id }) => id),
    { error: 'Selecione o nível de atenção' }
  ),
  clinical_course: z
    .enum(
      clinicalCourseOptions.map(({ id }) => id),
      { error: 'Selecione uma evolução válida' }
    )
    .or(z.literal(''))
    .optional(),
  pending_items: optionalText,
  alerts: optionalText,
  medias: z.array(z.any()).optional(),
})

export type EvolutionFormData = z.infer<typeof EvolutionSchema>
