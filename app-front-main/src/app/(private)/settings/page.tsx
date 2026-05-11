import { TopBar } from '@/components/TopBar'
import { HOSPITALIZATIONS } from '@/routes'

export default function Settings() {
  // TODO: configurações
  return (
    <TopBar>
      <TopBar.Back href={HOSPITALIZATIONS.PENDINGS} />
      <TopBar.Title>Configurações</TopBar.Title>
    </TopBar>
  )
}
