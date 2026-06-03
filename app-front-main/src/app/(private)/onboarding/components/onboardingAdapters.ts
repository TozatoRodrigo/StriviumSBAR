import { MemberType } from '@/constants/memberTypes'
import { HospitalizationPayload } from '@/hooks/mutations/hospitalizations'
import { PatientPayload } from '@/hooks/mutations/patients'
import { WorkspacePayload as InvitePayload } from '@/hooks/mutations/workspacesUser'
import { RolesHttpResponse } from '@/hooks/queries/roles'
import { splitFullname } from '@/lib/utils'
import { HospitalizationFormData } from '@/validations/hospitalization'
import { PatientFormData } from '@/validations/patient'

export const buildPatientPayload = (payload: PatientFormData): PatientPayload => {
  const { name, surname } = splitFullname(payload.full_name)

  return {
    first_name: name,
    last_name: surname,
    birth_date: payload.birth_date.toISOString().substring(0, 10),
    document_number: null,
  }
}

export const buildHospitalizationPayload = (
  payload: HospitalizationFormData,
  medicalTeamId: string
): HospitalizationPayload => ({
  medical_team_id: medicalTeamId,
  number: payload.number,
  place: payload.place,
  sector: payload.sector,
  reason: payload.reason,
  observations: payload.observations,
})

export const findDoctorRoleId = (roles: RolesHttpResponse[] = []) =>
  roles.find(role => role.name === 'doctor')?.id ?? null

export const buildDoctorInvitePayload = (email: string, roleId: string): InvitePayload => ({
  email,
  role_id: roleId,
  member_type: MemberType.DOCTOR,
})
