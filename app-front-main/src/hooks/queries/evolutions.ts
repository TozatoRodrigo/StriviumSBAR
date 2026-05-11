import api from '@/api/axios'
import { Paginated } from '@/types/common'
import { useQuery } from '@tanstack/react-query'

type EvolutionsParams = { search?: string }
type Evolutions = {
  params?: EvolutionsParams
  options?: { enabled?: boolean; keyword?: string }
}
export type EvolutionStatus = 'pending' | 'completed' | 'skipped' | 'canceled'
export type EvolutionType = 'hospitalization_visit' | 'hospitalization_discharge' | 'hospitalization_deceased'
export type EvolutionSbarPriority = 'routine' | 'attention' | 'critical'
export type EvolutionSbarClinicalCourse = 'improved' | 'stable' | 'worsened'
export type EvolutionSbar = {
  id: string
  situation: string
  background: string | null
  assessment: string
  recommendation: string
  priority: EvolutionSbarPriority
  clinical_course: EvolutionSbarClinicalCourse | null
  pending_items: string | null
  alerts: string | null
  created_at: string
  updated_at: string
}
export type EvolutionsHttpResponse = {
  id: string
  hospitalization_id: string
  user_id: string
  description: string
  status: EvolutionStatus
  type: EvolutionType
  user: { id: string; first_name: string; last_name: string; member_type: string | null }
  created_at: string
  updated_at: string
  medias?: Media[]
  sbar?: EvolutionSbar | null
}

export type MediaType = 'photo' | 'video' | 'audio'
export type Media = {
  id: string
  file_name: string
  file_path: string
  type: 'photo' | 'video' | 'audio'
}

export function useEvolutions(hospitalization_id: string, { params, options }: Evolutions = {}) {
  return useQuery<Paginated<EvolutionsHttpResponse[]>>({
    queryKey: ['evolutions', { hospitalization_id, keyword: options?.keyword, search: params?.search }],
    enabled: typeof options?.enabled !== 'undefined' ? options.enabled : true,
    queryFn: ({ signal }) =>
      api
        .get<Paginated<EvolutionsHttpResponse[]>>(
          `/hospitalization/v1/hospitalizations/${hospitalization_id}/hospitalization-actions`,
          { params, signal }
        )
        .then(({ data }) => data),
  })
}

export type EvolutionHttpResponse = {
  id: string
  hospitalization_id: string
  user_id: string
  description: string
  status: EvolutionStatus
  type: EvolutionType
  user: { id: string; first_name: string; last_name: string; member_type: string | null }
  created_at: string
  updated_at: string
  medias?: Media[]
  sbar?: EvolutionSbar | null
}

export function useEvolution(hospitalization_id: string, evolution_id: string, options: { enabled: boolean }) {
  return useQuery<EvolutionHttpResponse>({
    queryKey: ['evolution', { evolution_id }],
    enabled: options.enabled,
    // TODO: sempre invalidar
    queryFn: ({ signal }) =>
      api
        .get<EvolutionHttpResponse>(
          `/hospitalization/v1/hospitalizations/${hospitalization_id}/hospitalization-actions/${evolution_id}`,
          { signal }
        )
        .then(({ data }) => data),
  })
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
function withFakeEvolutions(
  data: Paginated<EvolutionsHttpResponse[]>,
  quantity: number
): Paginated<EvolutionsHttpResponse[]> {
  const fake: EvolutionsHttpResponse[] = Array.from({ length: quantity }).map((_, index) => ({
    id: crypto.randomUUID(),
    created_at: new Date().toISOString(),
    status: 'completed',
    type: 'hospitalization_deceased',
    hospitalization_id: crypto.randomUUID(),
    updated_at: new Date().toISOString(),
    user_id: crypto.randomUUID(),
    user: { id: crypto.randomUUID(), first_name: 'Leandro', last_name: 'Gomes - Fake', member_type: 'DOCTOR' },
    description: 'Paciente apresenta dor no estomago, refluxo e náusea.',
    medias:
      index % 2 == 0
        ? [
            {
              id: crypto.randomUUID(),
              file_name:
                'https://images.unsplash.com/photo-1530497610245-94d3c16cda28?q=80&w=764&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
              file_path:
                'https://images.unsplash.com/photo-1530497610245-94d3c16cda28?q=80&w=764&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
              type: 'photo',
            },
            {
              id: crypto.randomUUID(),
              file_name:
                'https://images.unsplash.com/photo-1516069677018-378515003435?q=80&w=1229&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
              file_path:
                'https://images.unsplash.com/photo-1516069677018-378515003435?q=80&w=1229&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
              type: 'photo',
            },
            {
              id: crypto.randomUUID(),
              file_name: 'https://dl.musopen.org/recordings/e9b07bfd-b8b0-40bc-8550-3cfb8629a7d6.mp3',
              file_path: 'https://dl.musopen.org/recordings/e9b07bfd-b8b0-40bc-8550-3cfb8629a7d6.mp3',
              type: 'audio',
            },
            {
              id: crypto.randomUUID(),
              file_name: 'https://assets.codepen.io/6093409/river.mp4',
              file_path: 'https://assets.codepen.io/6093409/river.mp4',
              type: 'video',
            },
            {
              id: crypto.randomUUID(),
              file_name: 'https://assets.codepen.io/6093409/river.mp4',
              file_path: 'https://assets.codepen.io/6093409/river.mp4',
              type: 'video',
            },
            {
              id: crypto.randomUUID(),
              file_name:
                'https://images.unsplash.com/photo-1618093877862-3630a08f737f?q=80&w=1176&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
              file_path:
                'https://images.unsplash.com/photo-1618093877862-3630a08f737f?q=80&w=1176&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
              type: 'photo',
            },
            {
              id: crypto.randomUUID(),
              file_name: 'https://dl.musopen.org/recordings/e9b07bfd-b8b0-40bc-8550-3cfb8629a7d6.mp3',
              file_path: 'https://dl.musopen.org/recordings/e9b07bfd-b8b0-40bc-8550-3cfb8629a7d6.mp3',
              type: 'audio',
            },
          ]
        : [],
  }))
  return { ...data, data: [...data.data, ...fake] }
}
