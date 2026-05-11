'use client'

import { useRouter } from 'next/navigation'

import { HOSPITALIZATIONS } from '@/routes'
import { useHospitalizationParams } from '@/hooks/queryParams/hospitalizations'
import { Detail } from './components/Detail'

export default function Hospitalization() {
  const { hospitalization_id } = useHospitalizationParams()
  const router = useRouter()
  if (!hospitalization_id) {
    router.push(HOSPITALIZATIONS.PENDINGS)
    return null
  }
  return <Detail hospitalization_id={hospitalization_id} />
}
