import { Paginated } from '@/types/common'

export function parseEnumType<T extends Record<string, string>>(value: string, enumObj: T): T[keyof T] | undefined {
  if (Object.values(enumObj).includes(value)) {
    return value as T[keyof T]
  }
  return undefined
}

export function withCallbackRoute(path: string, callback: string): string {
  let url: URL

  if (path.startsWith('http://') || path.startsWith('https://')) {
    url = new URL(path)
  } else {
    url = new URL(path, 'http://template.com')
  }

  url.searchParams.set('callback', callback)

  if (url.origin === 'http://template.com') {
    return url.pathname + url.search
  } else {
    return url.toString()
  }
}

export function withFormStepsParams(path: string, current_step: string, steps: string): string {
  let url: URL

  if (path.startsWith('http://') || path.startsWith('https://')) {
    url = new URL(path)
  } else {
    url = new URL(path, 'http://template.com')
  }

  url.searchParams.set('current_step', current_step)
  url.searchParams.set('steps', steps)

  if (url.origin === 'http://template.com') {
    return url.pathname + url.search
  } else {
    return url.toString()
  }
}

export function isValidCPF(cpf: string): boolean {
  cpf = cpf.replace(/[^\d]+/g, '')
  if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false

  const calcCheckDigit = (base: string, factor: number): number => {
    let total = 0
    for (let i = 0; i < base.length; i++) {
      total += parseInt(base[i]) * (factor - i)
    }
    const rest = (total * 10) % 11
    return rest === 10 ? 0 : rest
  }

  const firstCheck = calcCheckDigit(cpf.slice(0, 9), 10)
  const secondCheck = calcCheckDigit(cpf.slice(0, 10), 11)

  return firstCheck === parseInt(cpf[9]) && secondCheck === parseInt(cpf[10])
}

export function decodeJwt<T = Record<string, unknown>>(token: string): T | null {
  try {
    const [, payloadBase64] = token.split('.')

    if (!payloadBase64) return null

    const jsonPayload = atob(payloadBase64.replace(/-/g, '+').replace(/_/g, '/'))
    return JSON.parse(jsonPayload) as T
  } catch {
    return null
  }
}

export function splitFullname(fullName: string) {
  const slice = fullName.trim().split(/\s+/)
  const name = slice[0].trim()
  const surname = slice.slice(1).join(' ').trim()

  return { name, surname }
}

export function joinFullname(name: string, surname: string) {
  return `${name.trim()} ${surname.trim()}`
}

export function getNextPageParam(lastPage: Paginated<unknown>) {
  if (lastPage.page < lastPage.total_pages) return lastPage.page + 1

  return undefined
}
