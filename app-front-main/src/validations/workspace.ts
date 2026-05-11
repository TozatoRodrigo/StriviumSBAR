import { z } from 'zod/v4'

export const WorkspaceSchema = z.object({
  name: z
    .string()
    .trim()
    .min(3, 'Nome deve ter pelo menos 5 caracteres')
    .max(255, 'Nome deve ter no máximo 255 caracteres'),
})

export type WorkspaceFormData = z.infer<typeof WorkspaceSchema>
