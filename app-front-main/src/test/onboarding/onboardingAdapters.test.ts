import { describe, expect, it } from 'vitest'

import {
  buildHospitalizationPayload,
  buildPatientPayload,
  findDoctorRoleId,
} from '@/app/(private)/onboarding/components/onboardingAdapters'

describe('onboardingAdapters', () => {
  it('adapts patient form data to create payload', () => {
    const payload = buildPatientPayload({
      full_name: 'Joao da Silva',
      birth_date: new Date('2020-01-02T12:00:00.000Z'),
    })

    expect(payload).toEqual({
      first_name: 'Joao',
      last_name: 'da Silva',
      birth_date: '2020-01-02',
      document_number: null,
    })
  })

  it('injects medical team id into hospitalization payload', () => {
    const payload = buildHospitalizationPayload(
      {
        medical_team_id: '',
        number: 'NI-001',
        place: 'Hospital Central',
        sector: 'UTI',
        reason: 'Monitoramento',
        observations: 'Sem intercorrencias',
      },
      'team-123'
    )

    expect(payload).toEqual({
      medical_team_id: 'team-123',
      number: 'NI-001',
      place: 'Hospital Central',
      sector: 'UTI',
      reason: 'Monitoramento',
      observations: 'Sem intercorrencias',
    })
  })

  it('finds the doctor role id when available', () => {
    const roleId = findDoctorRoleId([
      { id: 'role-admin', name: 'admin', description: 'Administrador' },
      { id: 'role-doctor', name: 'doctor', description: 'Medico' },
    ])

    expect(roleId).toBe('role-doctor')
  })

  it('returns null when doctor role is missing', () => {
    const roleId = findDoctorRoleId([{ id: 'role-admin', name: 'admin', description: 'Administrador' }])

    expect(roleId).toBeNull()
  })
})
