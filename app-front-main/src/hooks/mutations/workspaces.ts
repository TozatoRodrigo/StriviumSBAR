import api from '@/api/axios'
import { useMutation } from '@tanstack/react-query'

type SigninPayload = {
  tenant_id: string
}

type SigninHttpResponse = {
  access_token: string
  refresh_token: string
}

export function useSigninWorkspaceMutation(onSuccess?: (data: SigninHttpResponse) => void) {
  return useMutation<SigninHttpResponse, Error, SigninPayload>({
    mutationFn: async (payload: SigninPayload) => {
      return api.post('/auth/v1/tenant', payload).then(({ data }) => data)
    },
    onSuccess,
  })
}

export type WorkspacePayload = {
  name: string
}

type WorkspaceCreateHttpRequest = {
  payload: WorkspacePayload
}

type WorkspaceHttpResponse = {
  id: string
  name: string
  birth_date: string
  cellphone: string
}

export function useCreateWorkspace() {
  return useMutation<WorkspaceHttpResponse, Error, WorkspaceCreateHttpRequest>({
    mutationFn: async ({ payload }: WorkspaceCreateHttpRequest) => {
      return api
        .post('/tenant/v1/tenants', payload, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
        .then(({ data }) => data)
    },
  })
}

type WorkspaceUpdateHttpRequest = { id: string } & WorkspaceCreateHttpRequest

export function useUpdateWorkspace() {
  return useMutation<WorkspaceHttpResponse, Error, WorkspaceUpdateHttpRequest>({
    mutationFn: async ({ id, payload }: WorkspaceUpdateHttpRequest) => {
      return api.patch(`/tenant/v1/tenants/${id}`, payload).then(data => data.data)
    },
  })
}

type WorkspaceRefreshTokenPayload = {
  refresh_token: string
}

type WorkspaceRefreshTokenHttpResponse = {
  access_token: string
  refresh_token: string
}

export function useWorkspaceRefreshToken(onSuccess?: (data: WorkspaceRefreshTokenHttpResponse) => void) {
  return useMutation<WorkspaceRefreshTokenHttpResponse, Error, WorkspaceRefreshTokenPayload>({
    mutationFn: async ({ refresh_token }: WorkspaceRefreshTokenPayload) => {
      return api
        .post<WorkspaceRefreshTokenHttpResponse>('/tenant/v1/refresh/tenant', { refresh_token })
        .then(data => data.data)
    },
    onSuccess,
  })
}
