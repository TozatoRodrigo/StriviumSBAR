import api from '@/api/axios'
import { useMutation } from '@tanstack/react-query'

export type TeamPayload = {
  name: string
  description: string
}

type TeamCreateHttpRequest = {
  payload: TeamPayload
}

type TeamUpdateHttpRequest = { id: string } & TeamCreateHttpRequest
type TeamDeleteHttpRequest = { id: string }

type TeamHttpResponse = {
  id: string
  name: string
  description: string
}

export function useCreateTeam() {
  return useMutation<TeamHttpResponse, Error, TeamCreateHttpRequest>({
    mutationFn: async ({ payload }: TeamCreateHttpRequest) => {
      return api.post('/medical-team/v1/medical-teams', payload).then(({ data }) => data)
    },
  })
}

export function useUpdateTeam() {
  return useMutation<TeamHttpResponse, Error, TeamUpdateHttpRequest>({
    mutationFn: async ({ id, payload }: TeamUpdateHttpRequest) => {
      return api.put(`/medical-team/v1/medical-teams/${id}`, payload).then(({ data }) => data)
    },
  })
}

export function useDeleteTeam() {
  return useMutation<unknown, Error, TeamDeleteHttpRequest>({
    mutationFn: async ({ id }: TeamDeleteHttpRequest) => {
      return api.delete(`/medical-team/v1/medical-teams/${id}`)
    },
  })
}
