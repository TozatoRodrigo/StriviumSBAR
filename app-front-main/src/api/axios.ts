import axios, { InternalAxiosRequestConfig } from 'axios'
import { AUTH_LOCAL_STORAGE_KEY } from '@/constants/auth'
import { WORKSPACE_LOCAL_STORAGE_KEY } from '@/constants/workspace'

export const apiOnlyAuth = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
})

apiOnlyAuth.interceptors.request.use(config => {
  const token = localStorage.getItem(AUTH_LOCAL_STORAGE_KEY)
  if (token) {
    config.headers.Authorization = mountBearer(token)
  }
  setTimezone(config)
  return config
})

export const apiWithoutInterceptors = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
})

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
})

api.interceptors.request.use(config => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = mountBearer(token)
  }
  setTimezone(config)
  return config
})

function setTimezone(config: InternalAxiosRequestConfig) {
  config.headers['X-Timezone'] = Intl.DateTimeFormat().resolvedOptions().timeZone ?? 'America/Sao_Paulo'
}

function getToken(): string | null {
  const workspaceToken = localStorage.getItem(WORKSPACE_LOCAL_STORAGE_KEY)
  const userToken = localStorage.getItem(AUTH_LOCAL_STORAGE_KEY)
  return workspaceToken || userToken || null
}

function mountBearer(token: string) {
  return `Bearer ${token}`
}

export default api
