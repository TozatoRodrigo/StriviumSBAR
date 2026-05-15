import api from '@/api/axios'
import { Paginated } from '@/types/common'
import { useQuery } from '@tanstack/react-query'

export type RolesHttpResponse = {
  id: string
  name: 'member' | 'admin' | 'doctor'
  description: string
}

export function useUserRoles() {
  return useQuery<Paginated<RolesHttpResponse[]>>({
    queryKey: ['user-roles'],
    queryFn: ({ signal }) => api.get('/tenant-user/v1/roles', { signal }).then(({ data }) => data),
  })
}
