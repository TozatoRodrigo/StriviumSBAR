import api from '@/api/axios'
import { useMutation } from '@tanstack/react-query'
import { MemberType } from '@/constants/memberTypes'

export type WorkspacePayload = {
  email: string
  role_id: string
  member_type?: MemberType
}

type WorkspaceInviteHttpRequest = {
  payload: WorkspacePayload
}

type WorkspaceInviteHttpResponse = object

export function useWorkspaceSendInvite() {
  return useMutation<WorkspaceInviteHttpResponse, Error, WorkspaceInviteHttpRequest>({
    mutationFn: async ({ payload }: WorkspaceInviteHttpRequest) => {
      return api.post('/tenant-user/v1/tenant-users/invite', payload).then(({ data }) => data)
    },
  })
}

type WorkspaceAcceptInviteHttpRequest = { id: string }

type WorkspaceAcceptInviteHttpResponse = {
  id: string
  email: string
  status: string
  created_at: string
  updated_at: string
}

export function useWorkspaceAcceptInvite() {
  return useMutation<WorkspaceAcceptInviteHttpResponse, Error, WorkspaceAcceptInviteHttpRequest>({
    mutationFn: async ({ id }: WorkspaceAcceptInviteHttpRequest) => {
      return api
        .post<WorkspaceAcceptInviteHttpResponse>(`/tenant-user/v1/tenant-users/accept-invite/${id}`)
        .then(data => data.data)
    },
  })
}

type WorkspaceDeclineInviteHttpRequest = { id: string }

type WorkspaceDeclineInviteHttpResponse = {
  id: string
  email: string
  status: string
  created_at: string
  updated_at: string
}

export function useWorkspaceDeclineInvite() {
  return useMutation<WorkspaceDeclineInviteHttpResponse, Error, WorkspaceDeclineInviteHttpRequest>({
    mutationFn: async ({ id }: WorkspaceDeclineInviteHttpRequest) => {
      return api
        .post<WorkspaceDeclineInviteHttpResponse>(`/tenant-user/v1/tenant-users/reject-invite/${id}`)
        .then(data => data.data)
    },
  })
}
