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

type DoctorUpdateHttpRequest = { id: number } & DoctorCreateHttpRequest
type DoctorDeleteHttpRequest = { id: string }

type DoctorHttpResponse = {
  id: number
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
      console.log('POST', `/doctors`, { payload })
      return new Promise(resolve =>
        setTimeout(
          () =>
            resolve({
              id: 1,
              full_name: '',
              birth_date: new Date().toISOString(),
              cellphone: '454645465',
              crm_number: '1234',
              crm_uf: 'PR',
              document: '88888',
              email: 'doctor@doctor.com',
              gender: 'male',
              specialty: 'CARDIOLOGY',
            }),
          3000
        )
      )
    },
  })
}

export function useUpdateDoctor() {
  return useMutation<DoctorHttpResponse, Error, DoctorUpdateHttpRequest>({
    mutationFn: async ({ id, payload }: DoctorUpdateHttpRequest) => {
      console.log('PATCH', `/doctors/${id}`, { payload })
      return new Promise(resolve =>
        setTimeout(
          () =>
            resolve({
              id: 1,
              full_name: '',
              birth_date: new Date().toISOString(),
              cellphone: '454645465',
              crm_number: '1234',
              crm_uf: 'PR',
              document: '88888',
              email: 'doctor@doctor.com',
              gender: 'male',
              specialty: 'CARDIOLOGY',
            }),
          3000
        )
      )
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
