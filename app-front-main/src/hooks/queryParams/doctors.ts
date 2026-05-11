import { useSearchParams } from 'next/navigation'
import { useRemoveParams } from './utils'

const keys = {
  doctor_id: 'doctor_id',
} as const

export const useDoctorParams = () => {
  const searchParams = useSearchParams()
  const removeParams = useRemoveParams()
  const doctor_id = searchParams.get(keys.doctor_id)

  const removeParam = (param: keyof typeof keys) => removeParams(param)

  return { doctor_id, keys, removeParam }
}
