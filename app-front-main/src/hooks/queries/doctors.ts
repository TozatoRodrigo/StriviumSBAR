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
    number: number
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

export function useDoctor(id: number | string, options: { enabled: boolean }) {
  return useQuery<DoctorHttpResponse>({
    ...options,
    queryKey: ['doctors', id],
    queryFn: () =>
      new Promise(resolve =>
        setTimeout(
          () =>
            resolve({
              id: 1,
              full_name: 'nome completo',
              birth_date: '2024-07-20T16:41:33.017Z',
              cellphone: '44034237989',
              crm_number: '1234',
              crm_uf: 'PR',
              document: '85915352006',
              email: 'doctor@doctor.com',
              gender: 'male',
              specialty: 'CARDIOLOGY',
            }),
          600
        )
      ),
  })
}
