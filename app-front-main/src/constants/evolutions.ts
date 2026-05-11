export const typeOptions = [
  { id: 'hospitalization_visit', label: 'Visita' },
  { id: 'hospitalization_discharge', label: 'Alta' },
  { id: 'hospitalization_deceased', label: 'Óbito' },
] as const

export const defaultEvolutionType = 'hospitalization_visit' as const

export const priorityOptions = [
  { id: 'routine', label: 'Rotina', description: 'sem alerta imediato' },
  { id: 'attention', label: 'Atenção', description: 'requer acompanhamento próximo' },
  { id: 'critical', label: 'Crítico', description: 'alto risco ou instabilidade' },
] as const

export const clinicalCourseOptions = [
  { id: 'improved', label: 'Melhorou' },
  { id: 'stable', label: 'Estável' },
  { id: 'worsened', label: 'Piorou' },
] as const
