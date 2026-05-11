import api from '@/api/axios'
import { Paginated } from '@/types/common'
import { useInfiniteQuery, useQuery } from '@tanstack/react-query'
import { getNextPageParam } from '@/lib/utils'

export type WorkspacesPendingInvitesHttpResponse = {
  data: {
    id: string
    email: string
    status: 'pending'
    created_at: string
    updated_at: string
    tenant_id: string
    tenant: {
      id: string
      name: string
    }
  }[]
}

export function useWorkspacesPendingInvites() {
  return useQuery<WorkspacesPendingInvitesHttpResponse, Error>({
    queryKey: ['workspaces-invites'],
    queryFn: async ({ signal }) =>
      api
        .get<WorkspacesPendingInvitesHttpResponse>('/tenant-user/v1/tenant-users/pending-invites', { signal })
        .then(({ data }) => data),
  })
}

export type WorkspacesPendingInvitesCountHttpResponse = {
  count: number
}

export function useWorkspacesPendingInvitesCount() {
  return useQuery<WorkspacesPendingInvitesCountHttpResponse, Error>({
    queryKey: ['workspaces-invites-count'],
    queryFn: async ({ signal }) =>
      api
        .get<WorkspacesPendingInvitesCountHttpResponse>('/tenant-user/v1/tenant-users/pending-invites/count', {
          signal,
        })
        .then(({ data }) => data),
    initialData: { count: 0 },
  })
}

type WorkspacesUsersParams = { search?: string; limit: number }

export type WorkspacesUsersHttpResponse = {
  id: string
  tenant_id: string
  user_id: string
  user: {
    id: string
    first_name: string
    last_name: string
    email: string
  }
  role_id: string
  role: {
    id: string
    name: string
    description: string
  }
  created_at: string
  updated_at: string
}

type WorkspacesUsersProps = {
  params?: WorkspacesUsersParams
  options?: { enabled?: boolean; keyword?: string }
}

export function useWorkspaceUsers({ params, options }: WorkspacesUsersProps = { params: { search: '', limit: 10 } }) {
  return useInfiniteQuery<Paginated<WorkspacesUsersHttpResponse[]>>({
    queryKey: ['workspace-users', { keyword: options?.keyword, search: params?.search }],
    initialPageParam: 1,
    queryFn: ({ pageParam, signal }) =>
      api
        .get<Paginated<WorkspacesUsersHttpResponse[]>>('/tenant-user/v1/tenant-users', {
          signal,
          params: { page: pageParam, limit: params?.limit, search: params?.search },
        })
        .then(({ data }) => data),
    getNextPageParam,
  })
}

type WorkspacePendingInvitesParams = { search?: string; limit: number }

export type WorkspacePendingInvitesHttpResponse = {
  id: string
  tenant_id: string
  tenant: {
    id: string
    name: string
    logo_url: string
  }
  role: {
    name: string
    description: string
  }
  email: string
  status: 'pending'
  created_at: string
  updated_at: string
}

type WorkspacePendingInvitesProps = {
  params?: WorkspacePendingInvitesParams
  options?: { enabled?: boolean; keyword?: string }
}

export function useWorkspacePendingInvites(
  { params, options }: WorkspacePendingInvitesProps = { params: { search: '', limit: 10 } }
) {
  return useInfiniteQuery<Paginated<WorkspacePendingInvitesHttpResponse[]>>({
    queryKey: ['workspace-invites', { keyword: options?.keyword, search: params?.search }],
    initialPageParam: 1,
    queryFn: ({ pageParam, signal }) =>
      api
        .get<Paginated<WorkspacePendingInvitesHttpResponse[]>>('/tenant-user/v1/tenant-users/invites', {
          signal,
          params: { page: pageParam, limit: params?.limit, search: params?.search },
        })
        .then(({ data }) => data),
    getNextPageParam,
  })
}
