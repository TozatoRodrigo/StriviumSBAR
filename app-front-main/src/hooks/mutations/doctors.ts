import api from '@/api/axios'
import { useMutation } from '@tanstack/react-query'

export type DoctorPayload = {
  full_name: string
  birth_date: string
  cellphone: string
  gender: 'male' | 'female' | 'other'
  document: string
  email: string
  specialty: string
  crm_uf: string
  crm_number: string
}

export type DoctorCreateHttpRequest = {
  payload: DoctorPayload
}

type DoctorUpdateHttpRequest = { id: string } & DoctorCreateHttpRequest
type DoctorDeleteHttpRequest = { id: string }

type DoctorHttpResponse = {
  id: string
  full_name: string
  birth_date: string
  cellphone: string
  gender: string
  document: string
  email: string
  specialty: string
  crm_uf: string
  crm_number: string
}

export function useCreateDoctor() {
  return useMutation<DoctorHttpResponse, Error, DoctorCreateHttpRequest>({
    mutationFn: async ({ payload }: DoctorCreateHttpRequest) => {
      return api.post('/doctor/v1/doctors', payload).then(({ data }) => data)
    },
  })
}

export function useUpdateDoctor() {
  return useMutation<DoctorHttpResponse, Error, DoctorUpdateHttpRequest>({
    mutationFn: async ({ id, payload }: DoctorUpdateHttpRequest) => {
      return api.put(`/doctor/v1/doctors/${id}`, payload).then(({ data }) => data)
    },
  })
}

export function useDeleteDoctor() {
  return useMutation<unknown, Error, DoctorDeleteHttpRequest>({
    mutationFn: async ({ id }: DoctorDeleteHttpRequest) => {
      return api.delete(`/doctor/v1/doctors/${id}`)
    },
  })
}
