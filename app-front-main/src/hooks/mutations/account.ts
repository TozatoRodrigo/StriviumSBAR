import api from '@/api/axios'
import { Headers } from '@/types/common'
import { useMutation } from '@tanstack/react-query'

export type SignupPayload = {
  first_name: string
  last_name: string
  crm_state?: string | null
  crm_number?: string | null
  document?: string | null
  email: string
  password: string
  birth_date: string
}

type SignupHttpResponse = {
  id: string
  first_name: string
  last_name: string
  crm_state: string | null
  crm_number: string | null
  document: string | null
  email: string
  birth_date: string
}

export type SignupMutationProps = {
  payload: SignupPayload
  headers: Headers
}

export function useSignupMutation(onSuccess?: (data: SignupHttpResponse) => void) {
  return useMutation<SignupHttpResponse, Error, SignupMutationProps>({
    mutationFn: async (props: SignupMutationProps) => {
      return api
        .post<SignupHttpResponse>('/user/v1/users', props.payload, { headers: props.headers })
        .then(data => data.data)
    },
    onSuccess,
  })
}
