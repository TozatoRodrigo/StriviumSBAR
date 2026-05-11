import { useSearchParams } from 'next/navigation'
import { useRemoveParams } from './utils'

const keys = {
  evolution_id: 'evolution_id',
} as const

export const useEvolutionParams = () => {
  const searchParams = useSearchParams()
  const removeParams = useRemoveParams()
  const evolution_id = searchParams.get(keys.evolution_id)

  const removeParam = (param: keyof typeof keys) => removeParams(param)

  return { evolution_id, keys, removeParam }
}
