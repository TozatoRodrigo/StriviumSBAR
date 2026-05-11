import { useSearchParams } from 'next/navigation'
import { useRemoveParams } from './utils'

const keys = {
  team_id: 'team_id',
} as const

export const useTeamParams = () => {
  const searchParams = useSearchParams()
  const removeParams = useRemoveParams()
  const team_id = searchParams.get(keys.team_id)

  const removeParam = (param: keyof typeof keys) => removeParams(param)

  return { team_id, keys, removeParam }
}
