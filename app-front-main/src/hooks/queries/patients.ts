import { useQuery } from '@tanstack/react-query'
import { Paginated } from '@/types/common'
import api from '@/api/axios'

export type PatientsHttpResponse = {
  id: string
  first_name: string
  last_name: string
  document_number?: string
  birth_date: string
}

type PatientsParams = { search: string }
type Patients = {
  params?: PatientsParams
  options?: { enabled?: boolean; keyword?: string }
}

export function usePatients({ params, options }: Patients = { params: { search: '' } }) {
  return useQuery<Paginated<PatientsHttpResponse[]>>({
    queryKey: ['patients', { keyword: options?.keyword, search: params?.search }],
    enabled: typeof options?.enabled !== 'undefined' ? options.enabled : true,
    queryFn: ({ signal }) => api.get('/patient/v1/patients', { params, signal }).then(({ data }) => data),
  })
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
function patientsWithFake(
  data: Paginated<PatientsHttpResponse[]>,
  quantity: number
): Paginated<PatientsHttpResponse[]> {
  const fake_patient_infos: PatientsHttpResponse[] = Array.from({ length: quantity }).map((_, index) => ({
    id: index.toString(),
    first_name: 'Marcos',
    last_name: 'de Paula - Fake',
    birth_date: new Date().toISOString(),
  }))

  return { ...data, data: [...data.data, ...fake_patient_infos] }
}

type PatientByIdHttpResponse = {
  id: number
  first_name: string
  last_name: string
  document_number: string
  birth_date: string
}

export function usePatientById(id: string, options: { enabled: boolean }) {
  return useQuery<PatientByIdHttpResponse>({
    ...options,
    queryKey: ['patient', id],
    queryFn: async ({ signal }) =>
      api.get<PatientByIdHttpResponse>(`/patient/v1/patients/${id}`, { signal }).then(({ data }) => data),
  })
}
