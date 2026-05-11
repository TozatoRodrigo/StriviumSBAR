import z from 'zod/v4'
import { MemberType } from '@/constants/memberTypes'

export const WorkspaceInviteSchema = z
  .object({
    email: z.email('Informe um email válido'),
    role_id: z.string().min(1, 'Permissão obrigatória'),
    member_type: z.enum(MemberType).optional(),
    role_name: z.string().optional(),
  })
  .refine(
    data => {
      if (data.role_name === 'member') {
        return !!data.member_type && data.member_type.length > 0
      }
      return true
    },
    {
      message: 'Tipo de membro obrigatório',
      path: ['member_type'],
    }
  )

export type InviteFormData = z.infer<typeof WorkspaceInviteSchema>
