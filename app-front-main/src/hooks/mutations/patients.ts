import api from '@/api/axios'
import { useMutation } from '@tanstack/react-query'

export type PatientPayload = {
  first_name: string
  last_name: string
  birth_date: string
  document_number: string | null
}

type PatientCreateHttpRequest = {
  payload: PatientPayload
}

type PatientUpdateHttpRequest = { id: string } & PatientCreateHttpRequest
type PatientDeleteHttpRequest = { id: string }

type PatientHttpResponse = {
  id: string
  first_name: string
  last_name: string
  birth_date: string
  document_number?: string
  cellphone: string
}

export function useCreatePatient() {
  return useMutation<PatientHttpResponse, Error, PatientCreateHttpRequest>({
    mutationFn: async ({ payload }: PatientCreateHttpRequest) => {
      return api.post('/patient/v1/patients', payload).then(({ data }) => data)
    },
  })
}

export function useUpdatePatient() {
  return useMutation<PatientHttpResponse, Error, PatientUpdateHttpRequest>({
    mutationFn: async ({ id, payload }: PatientUpdateHttpRequest) => {
      return api.put(`/patient/v1/patients/${id}`, payload).then(({ data }) => data)
    },
  })
}

export function useDeletePatient() {
  return useMutation<unknown, Error, PatientDeleteHttpRequest>({
    mutationFn: async ({ id }: PatientDeleteHttpRequest) => {
      return api.delete(`/patient/v1/patients/${id}`)
    },
  })
}
