import { useSearchParams } from 'next/navigation'

export const useHospitalizationParams = () => {
  const searchParams = useSearchParams()
  const hospitalization_id = searchParams.get('hospitalization_id')

  return { hospitalization_id }
}
