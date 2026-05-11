const HOSPITALIZATIONS_BASE = '/hospitalizations'
const HOSPITALIZATIONS = {
  EDIT(id: string): string {
    return `${HOSPITALIZATIONS_BASE}/${id}/edit`
  },
  get CREATE(): string {
    return `${HOSPITALIZATIONS_BASE}/create`
  },
  get DONE(): string {
    return `${HOSPITALIZATIONS_BASE}/done`
  },
  get PENDINGS(): string {
    return `${HOSPITALIZATIONS_BASE}/pendings`
  },
  EVOLUTIONS: {
    LIST(hospitalization_id: string): string {
      return `${HOSPITALIZATIONS_BASE}/${hospitalization_id}/evolutions`
    },
    GET(hospitalization_id: string, evolution_id: string): string {
      return `${HOSPITALIZATIONS_BASE}/${hospitalization_id}/evolutions/${evolution_id}`
    },
    CREATE(hospitalization_id: string): string {
      return `${HOSPITALIZATIONS_BASE}/${hospitalization_id}/evolutions/create`
    },
  },
}

export { HOSPITALIZATIONS }
