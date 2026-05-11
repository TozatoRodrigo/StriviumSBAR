import { useSearchParams } from 'next/navigation'
import { useRemoveParams } from './utils'

const keys = {
  workspace_id: 'workspace_id',
  modal: 'modal',
} as const

export const useWorkspacesParams = () => {
  const searchParams = useSearchParams()
  const removeParams = useRemoveParams()
  const workspace_id = searchParams.get(keys.workspace_id)
  const modal = searchParams.get(keys.modal)
  const removeParam = (param: keyof typeof keys) => removeParams(param)

  return { workspace_id, modal, keys, removeParam }
}
