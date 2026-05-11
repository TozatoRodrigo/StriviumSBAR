import { TopBar } from '@/components/TopBar'
import { HOSPITALIZATIONS } from '@/routes'

export default function Subscriptions() {
  return (
    <TopBar>
      <TopBar.Back href={HOSPITALIZATIONS.PENDINGS} />
      <TopBar.Title>Assinaturas</TopBar.Title>
    </TopBar>
  )
}
