export enum MemberType {
  DOCTOR = 'doctor',
  NURSE = 'nurse',
  PHYSIOTHERAPIST = 'physiotherapist',
  NUTRITIONIST = 'nutritionist',
  PSYCHOLOGIST = 'psychologist',
  ADMINISTRATIVE_ASSISTANT = 'administrative_assistant',
  SPEECH_THERAPIST = 'speech_therapist',
  DENTIST = 'dentist',
  SOCIAL_WORKER = 'social_worker',
  RADIOLOGIST = 'radiologist',
  OCCUPATIONAL_THERAPIST = 'occupational_therapist',
}

export const memberTypeLabels: Record<MemberType, string> = {
  [MemberType.DOCTOR]: 'Médico',
  [MemberType.NURSE]: 'Enfermeiro',
  [MemberType.PHYSIOTHERAPIST]: 'Fisioterapeuta',
  [MemberType.NUTRITIONIST]: 'Nutricionista',
  [MemberType.PSYCHOLOGIST]: 'Psicólogo',
  [MemberType.ADMINISTRATIVE_ASSISTANT]: 'Assistente Administrativo',
  [MemberType.SPEECH_THERAPIST]: 'Fonoaudiólogo',
  [MemberType.DENTIST]: 'Odontólogo',
  [MemberType.SOCIAL_WORKER]: 'Assistente Social',
  [MemberType.RADIOLOGIST]: 'Radiologista',
  [MemberType.OCCUPATIONAL_THERAPIST]: 'Terapeuta Ocupacional',
}

export const memberTypesOptions = Object.entries(memberTypeLabels).map(([value, label]) => ({
  id: value as MemberType,
  name: label,
}))
