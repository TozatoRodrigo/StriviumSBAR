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

export function resolveSbarExtractEndpoint(baseUrl: string | undefined): string {
  const normalizedBaseUrl = (baseUrl || '').replace(/\/+$/, '').toLowerCase()
  return normalizedBaseUrl.endsWith('/api') ? '/sbar/extract' : '/api/sbar/extract'
}

export function useExtractSbar() {
  const endpoint = resolveSbarExtractEndpoint(process.env.NEXT_PUBLIC_API_URL)

  return useMutation<SbarExtractResponse, Error, ExtractSbarPayload>({
    mutationFn: async payload => {
      return api.post<SbarExtractResponse>(endpoint, payload).then(({ data }) => data)
    },
  })
}
