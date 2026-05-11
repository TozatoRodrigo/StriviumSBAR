import { apiOnlyAuth } from '@/api/axios'
import { useQuery } from '@tanstack/react-query'

export type UserInfoHttpResponse = {
  id: string
  first_name: string
  last_name: string
  crm?: string
  document?: string
  email: string
  birth_date: string
}

export function useUser({ enabled }: { enabled: boolean }) {
  return useQuery<UserInfoHttpResponse>({
    queryKey: ['user-info'],
    queryFn: async ({ signal }) =>
      apiOnlyAuth.get<UserInfoHttpResponse>('/user/v1/users/info', { signal }).then(({ data }) => data),
    staleTime: Infinity,
    enabled,
  })
}
