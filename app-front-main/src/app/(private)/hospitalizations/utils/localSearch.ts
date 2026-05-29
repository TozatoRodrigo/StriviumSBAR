import { HospitalizationInfo } from '@/components/Hospitalizations'
import { joinFullname } from '@/lib/utils'

function normalizeSearchText(value: string): string {
  return value
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim()
}

function buildHospitalizationSearchIndex(hospitalization: HospitalizationInfo): string {
  const fullName = joinFullname(hospitalization.patient.first_name, hospitalization.patient.last_name)

  return normalizeSearchText([fullName, hospitalization.sector, hospitalization.reason, hospitalization.place].join(' '))
}

export function filterHospitalizationsBySearch(
  hospitalizations: HospitalizationInfo[],
  search: string
): HospitalizationInfo[] {
  const normalizedSearch = normalizeSearchText(search)

  if (!normalizedSearch) return hospitalizations

  return hospitalizations.filter(hospitalization =>
    buildHospitalizationSearchIndex(hospitalization).includes(normalizedSearch)
  )
}

