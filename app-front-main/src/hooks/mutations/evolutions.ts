import api from '@/api/axios'
import { useMutation } from '@tanstack/react-query'

// TODO: em tipagens de raw(api), utilizar somente tipos primitivos

export type EvolutionPayload = FormData

type EvolutionCreateHttpRequest = {
  hospitalization_id: string
  payload: EvolutionPayload
}

type EvolutionUpdateHttpRequest = { id: string } & EvolutionCreateHttpRequest

type EvolutionHttpResponse = {
  id: string
  description: string
  images: string[] | null
  recording: string | null
}

export function useCreateEvolution() {
  return useMutation<EvolutionHttpResponse, Error, EvolutionCreateHttpRequest>({
    mutationFn: async ({ hospitalization_id, payload }: EvolutionCreateHttpRequest) => {
      return api
        .post<EvolutionHttpResponse>(
          `/hospitalization/v1/hospitalizations/${hospitalization_id}/hospitalization-actions`,
          payload
        )
        .then(({ data }) => data)
    },
  })
}

export function useUpdateEvolution() {
  return useMutation<EvolutionHttpResponse, Error, EvolutionUpdateHttpRequest>({
    mutationFn: async ({ id, hospitalization_id, payload }: EvolutionUpdateHttpRequest) => {
      return api
        .put<EvolutionHttpResponse>(
          `/hospitalization/v1/hospitalizations/${hospitalization_id}/hospitalization-actions/${id}`,
          payload
        )
        .then(({ data }) => data)
    },
  })
}
