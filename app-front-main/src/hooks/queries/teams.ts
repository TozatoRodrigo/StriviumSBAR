import api from '@/api/axios'
import { Paginated } from '@/types/common'
import { useInfiniteQuery, useQuery } from '@tanstack/react-query'
import { getNextPageParam } from '@/lib/utils'

export type TeamsHttpResponse = {
  id: string
  name: string
  description: string
}

type TeamsParams = { search?: string; limit?: number }

type Teams = {
  params?: TeamsParams
  options?: { enabled?: boolean; keyword?: string }
}

export function useTeams({ params, options }: Teams = {}) {
  return useInfiniteQuery<Paginated<TeamsHttpResponse[]>>({
    queryKey: ['teams', { keyword: options?.keyword, search: params?.search }],
    enabled: typeof options?.enabled !== 'undefined' ? options.enabled : true,
    queryFn: ({ signal, pageParam }) =>
      api
        .get<Paginated<TeamHttpResponse[]>>(`/medical-team/v1/medical-teams`, {
          signal,
          params: { limit: params?.limit, search: params?.search, page: pageParam },
        })
        .then(({ data }) => data),
    initialPageParam: 1,
    getNextPageParam,
  })
}

export type TeamHttpResponse = {
  id: string
  name: string
  description: string
}

export function useTeam(id: string, options: { enabled: boolean }) {
  return useQuery<TeamHttpResponse>({
    ...options,
    queryKey: ['team', id],
    queryFn: ({ signal }) =>
      api.get<TeamHttpResponse>(`/medical-team/v1/medical-teams/${id}`, { signal }).then(({ data }) => data),
  })
}
