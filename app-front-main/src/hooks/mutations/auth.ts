import api from '@/api/axios'
import { Headers } from '@/types/common'
import { useMutation } from '@tanstack/react-query'

export type SigninPayload = {
  login: string
  password: string
}

type SigninHttpResponse = {
  access_token: string
  refresh_token: string
}

export type SigninMutationProps = {
  payload: SigninPayload
  headers: Headers
}

export function useSigninMutation(onSuccess?: (data: SigninHttpResponse) => void) {
  return useMutation<SigninHttpResponse, Error, SigninMutationProps>({
    mutationFn: async (props: SigninMutationProps) => {
      return api
        .post<SigninHttpResponse>('/auth/v1/login', props.payload, { headers: props.headers })
        .then(data => data.data)
    },
    onSuccess,
  })
}

type UserRefreshTokenPayload = {
  refresh_token: string
}

type UserRefreshTokenHttpResponse = {
  access_token: string
  refresh_token: string
}

export function useUserRefreshToken(onSuccess?: (data: UserRefreshTokenHttpResponse) => void) {
  return useMutation<UserRefreshTokenHttpResponse, Error, UserRefreshTokenPayload>({
    mutationFn: async ({ refresh_token }: UserRefreshTokenPayload) => {
      return api.post<UserRefreshTokenHttpResponse>('/auth/v1/refresh/user', { refresh_token }).then(data => data.data)
    },
    onSuccess,
  })
}
