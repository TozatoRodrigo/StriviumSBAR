import { TopBar } from '@/components/TopBar'
import { HOSPITALIZATIONS } from '@/routes'

export default function Plans() {
  // TODO: planos
  return (
    <TopBar>
      <TopBar.Back href={HOSPITALIZATIONS.PENDINGS} />
      <TopBar.Title>Planos</TopBar.Title>
    </TopBar>
  )
}
