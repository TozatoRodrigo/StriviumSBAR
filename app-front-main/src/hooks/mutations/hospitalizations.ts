import api from '@/api/axios'
import { useMutation } from '@tanstack/react-query'

export type HospitalizationPayload = {
  medical_team_id: string
  number: string
  place: string
  sector: string
  reason: string
  observations?: string | undefined
}

type HospitalizationCreateHttpRequest = {
  patient_id: string
  payload: HospitalizationPayload
}

type HospitalizationUpdateHttpRequest = { id: string } & HospitalizationCreateHttpRequest
type HospitalizationDeleteHttpRequest = { id: string }

type HospitalizationHttpResponse = {
  id: number
  medical_team_id: number
  number: string
  place: string
  sector: string
  reason: string
  observations?: string | undefined
}

export function useCreateHospitalization() {
  return useMutation<HospitalizationHttpResponse, Error, HospitalizationCreateHttpRequest>({
    mutationFn: async ({ patient_id, payload }: HospitalizationCreateHttpRequest) => {
      const data = { patient_id, ...payload }
      return api.post('/hospitalization/v1/hospitalizations', data)
    },
  })
}

export function useUpdateHospitalization() {
  return useMutation<HospitalizationHttpResponse, Error, HospitalizationUpdateHttpRequest>({
    mutationFn: async ({ id, patient_id, payload }: HospitalizationUpdateHttpRequest) => {
      const data = { patient_id, ...payload }
      return api.put(`/hospitalization/v1/hospitalizations/${id}`, data)
    },
  })
}

export function useDeleteHospitalization() {
  return useMutation<unknown, Error, HospitalizationDeleteHttpRequest>({
    mutationFn: async ({ id }: HospitalizationDeleteHttpRequest) => {
      return api.delete(`/hospitalization/v1/hospitalizations/${id}`)
    },
  })
}
