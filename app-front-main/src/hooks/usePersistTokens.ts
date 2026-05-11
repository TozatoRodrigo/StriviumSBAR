import { useState } from 'react'

type Tokens = {
  access: string | null
  refresh: string | null
}

type NonNullableTokens = {
  [K in keyof Tokens]: NonNullable<Tokens[K]>
}

export const usePersistTokens = (accessKey: string, refreshKey: string) => {
  const [tokens, setTokens] = useState<Tokens | null>({
    access: typeof window !== 'undefined' ? localStorage.getItem(accessKey) : null,
    refresh: typeof window !== 'undefined' ? localStorage.getItem(refreshKey) : null,
  })

  const addTokens = ({ access, refresh }: NonNullableTokens) => {
    localStorage.setItem(accessKey, access)
    localStorage.setItem(refreshKey, refresh)
    setTokens({ access, refresh })
  }

  const clear = () => {
    localStorage.removeItem(accessKey)
    localStorage.removeItem(refreshKey)
    setTokens(null)
  }

  return { tokens, addTokens, clear }
}
