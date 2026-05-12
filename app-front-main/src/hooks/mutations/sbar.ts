import api from '@/api/axios'
import { useMutation } from '@tanstack/react-query'

export type SbarConfidence = {
  situation: number
  background: number
  assessment: number
  recommendation: number
  plan: number
}

export type SbarExtractResponse = {
  situation: string
  background: string
  assessment: string
  recommendation: string
  plan: string
  missing_information: string[]
  warnings: string[]
  confidence: SbarConfidence
}

type ExtractSbarPayload = {
  transcript: string
  context?: {
    hospitalization_id?: string
  }
}

export function useExtractSbar() {
  return useMutation<SbarExtractResponse, Error, ExtractSbarPayload>({
    mutationFn: async payload => {
      return api.post<SbarExtractResponse>('/api/sbar/extract', payload).then(({ data }) => data)
    },
  })
}
