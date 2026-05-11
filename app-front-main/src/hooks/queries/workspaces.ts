import api from '@/api/axios'
import { useQuery } from '@tanstack/react-query'

export type WorkspacesHttpResponse = {
  data: { id: string; name: string }[]
}

type WorkspacesParams = { search?: string }

export function useWorkspaces({ search }: WorkspacesParams = {}) {
  return useQuery<WorkspacesHttpResponse, Error>({
    queryKey: ['workspaces', { search }],
    queryFn: async ({ signal }) =>
      api
        .get<WorkspacesHttpResponse>('/tenant/v1/tenants/available-for-user', { signal, params: { search } })
        .then(({ data }) => data),
  })
}

export type WorkspaceHttpResponse = {
  id: string
  name: string
  logo_url: string
  created_at: string
  updated_at: string
}

export function useWorkspace(id: string, options?: { enabled?: boolean }) {
  return useQuery<WorkspaceHttpResponse>({
    ...(!!options && options),
    queryKey: ['workspace', 'info', id],
    queryFn: async ({ signal }) =>
      api.get<WorkspaceHttpResponse>(`/tenant/v1/tenants/${id}`, { signal }).then(({ data }) => data),
  })
}
