import { useSearchParams } from 'next/navigation'
import { useRemoveParams } from './utils'

const keys = {
  patient_id: 'patient_id',
} as const

export const usePatientParams = () => {
  const searchParams = useSearchParams()
  const removeParams = useRemoveParams()
  const patient_id = searchParams.get(keys.patient_id)

  const removeParam = (param: keyof typeof keys) => removeParams(param)

  return { patient_id, keys, removeParam }
}
