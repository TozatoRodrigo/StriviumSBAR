import { useQuery, useInfiniteQuery } from '@tanstack/react-query'
import { Paginated } from '@/types/common'
import api from '@/api/axios'
import { getNextPageParam } from '@/lib/utils'

export type HospitalizationStatus = 'active' | 'discharged' | 'deceased'

export type HospitalizationsHttpResponse = {
  id: string
  created_at: string
  sector: string
  reason: string
  place: string
  status: HospitalizationStatus
  patient: {
    id: string
    first_name: string
    last_name: string
  }
}

export function usePendings(limit = 10) {
  return useInfiniteQuery<Paginated<HospitalizationsHttpResponse[]>>({
    queryKey: ['hospitalizations', 'pendings'],
    initialPageParam: 1,
    queryFn: ({ pageParam, signal }) =>
      api
        .get<Paginated<HospitalizationsHttpResponse[]>>(`/hospitalization/v1/hospitalizations/pendings`, {
          signal,
          params: { page: pageParam, limit },
        })
        .then(({ data }) => data),
    getNextPageParam,
  })
}

export function useDone(limit = 10) {
  return useInfiniteQuery<Paginated<HospitalizationsHttpResponse[]>>({
    queryKey: ['hospitalizations', 'done'],
    initialPageParam: 1,
    queryFn: ({ pageParam, signal }) =>
      api
        .get<Paginated<HospitalizationsHttpResponse[]>>('/hospitalization/v1/hospitalizations/completed', {
          signal,
          params: { page: pageParam, limit },
        })
        .then(({ data }) => data),
    getNextPageParam,
  })
}

type HospitalizationsParams = { search: string; limit: number; patient_id?: string }
type Hospitalizations = {
  params?: HospitalizationsParams
  options?: { enabled?: boolean; keyword?: string }
}

export function useHospitalizations({ params, options }: Hospitalizations = { params: { search: '', limit: 10 } }) {
  return useInfiniteQuery<Paginated<HospitalizationsHttpResponse[]>>({
    queryKey: [
      'hospitalizations',
      { keyword: options?.keyword, search: params?.search, patient_id: params?.patient_id },
    ],
    initialPageParam: 1,
    enabled: typeof options?.enabled !== 'undefined' ? options.enabled : true,
    queryFn: ({ pageParam, signal }) =>
      api
        .get('/hospitalization/v1/hospitalizations', { params: { ...params, page: pageParam }, signal })
        .then(({ data }) => data),
    getNextPageParam,
  })
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
function withFakeHospitalizations(
  data: Paginated<HospitalizationsHttpResponse[]>,
  quantity: number = 1
): Paginated<HospitalizationsHttpResponse[]> {
  const fake_patient_infos: HospitalizationsHttpResponse[] = Array.from({ length: quantity }).map(() => ({
    id: crypto.randomUUID(),
    patient: {
      id: crypto.randomUUID(),
      first_name: 'Marcos',
      last_name: 'de Paula - Fake',
    },
    created_at: new Date().toISOString(),
    sector: 'Enfermaria',
    reason: 'Acompanhamento pós-cirurgia...',
    place: 'Cardiologia',
    status: 'active',
  }))

  return { ...data, data: [...data.data, ...fake_patient_infos] }
}

export type HospitalizationByIdHttpResponse = {
  id: string
  user_id: string
  patient_id: string
  medical_team_id: string
  created_at: string
  patient: {
    id: string
    first_name: string
    last_name: string
  }
  sector: string
  reason: string
  place: string
  number: string
  status: HospitalizationStatus
  observation: string
}

export function useHospitalization(id: string, options: { enabled?: boolean } = {}) {
  return useQuery<HospitalizationByIdHttpResponse>({
    ...options,
    queryKey: ['hospitalization', id],
    queryFn: ({ signal }) =>
      api
        .get<HospitalizationByIdHttpResponse>(`/hospitalization/v1/hospitalizations/${id}`, { signal })
        .then(({ data }) => data),
  })
}
