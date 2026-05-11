import { z } from 'zod/v4'

export const HospitalizationSchema = z.object({
  medical_team_id: z.coerce.string().min(1, 'Equipe obrigatória'),
  number: z.string().min(1, 'Número de Internação obrigatório'),
  place: z.string().min(1, 'Local obrigatório'),
  sector: z.string().min(1, 'Setor obrigatório'),
  reason: z.string().min(1, 'Motivo obrigatório'),
  observations: z.string().optional(),
})

export type HospitalizationFormData = z.infer<typeof HospitalizationSchema>
