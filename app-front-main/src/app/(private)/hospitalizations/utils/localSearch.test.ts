import { describe, expect, it } from 'vitest'

import { HospitalizationInfo } from '@/components/Hospitalizations'
import { filterHospitalizationsBySearch } from './localSearch'

const hospitalizations: HospitalizationInfo[] = [
  {
    id: 'h1',
    created_at: '2026-05-15T12:00:00Z',
    sector: 'UTI',
    reason: 'Inflamação pulmonar',
    place: 'Cardiologia',
    status: 'active',
    patient: { first_name: 'João', last_name: 'Silva' },
  },
  {
    id: 'h2',
    created_at: '2026-05-15T13:00:00Z',
    sector: 'Enfermaria',
    reason: 'Dor abdominal',
    place: 'Clínica Médica',
    status: 'discharged',
    patient: { first_name: 'Maria', last_name: 'Souza' },
  },
]

describe('filterHospitalizationsBySearch', () => {
  it('returns all items when search is empty', () => {
    expect(filterHospitalizationsBySearch(hospitalizations, '')).toHaveLength(2)
  })

  it('finds by patient name ignoring accents and casing', () => {
    const result = filterHospitalizationsBySearch(hospitalizations, 'joao')
    expect(result).toHaveLength(1)
    expect(result[0].id).toBe('h1')
  })

  it('finds by sector', () => {
    const result = filterHospitalizationsBySearch(hospitalizations, 'enfermaria')
    expect(result).toHaveLength(1)
    expect(result[0].id).toBe('h2')
  })

  it('finds by reason', () => {
    const result = filterHospitalizationsBySearch(hospitalizations, 'inflamacao')
    expect(result).toHaveLength(1)
    expect(result[0].id).toBe('h1')
  })

  it('finds by place', () => {
    const result = filterHospitalizationsBySearch(hospitalizations, 'clínica médica')
    expect(result).toHaveLength(1)
    expect(result[0].id).toBe('h2')
  })
})

