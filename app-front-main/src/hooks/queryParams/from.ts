'use client'

import { HOSPITALIZATIONS } from '@/routes'
import { useSearchParams } from 'next/navigation'

export const useFromQuery = (defaultBackHref: string = HOSPITALIZATIONS.PENDINGS) => {
  const searchParams = useSearchParams()
  const from = searchParams.get('from')

  const backHref = from || defaultBackHref
  const fromQuery = from ? `from=${from}` : ''

  return { from, backHref, fromQuery }
}

