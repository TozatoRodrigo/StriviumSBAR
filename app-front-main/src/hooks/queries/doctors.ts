import api from '@/api/axios'
import { Paginated } from '@/types/common'
import { useQuery } from '@tanstack/react-query'

type DoctorsParams = { search: string }
type Doctors = {
  params?: DoctorsParams
  options?: { enabled?: boolean; keyword?: string }
}

export type DoctorsHttpResponse = {
  id: string
  first_name: string
  last_name: string
  crm: {
    uf: string
    number: string
  }
}

export function useDoctors({ params, options }: Doctors = { params: { search: '' } }) {
  return useQuery<Paginated<DoctorsHttpResponse[]>>({
    queryKey: ['doctors', { keyword: options?.keyword, search: params?.search }],
    enabled: typeof options?.enabled !== 'undefined' ? options.enabled : true,
    queryFn: ({ signal }) => api.get('/doctor/v1/doctors', { params, signal }).then(({ data }) => data),
  })
}

export type DoctorHttpResponse = {
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

export function useDoctor(id: string, options: { enabled: boolean }) {
  return useQuery<DoctorHttpResponse>({
    ...options,
    queryKey: ['doctors', id],
    queryFn: ({ signal }) => api.get(`/doctor/v1/doctors/${id}`, { signal }).then(({ data }) => data),
  })
}
