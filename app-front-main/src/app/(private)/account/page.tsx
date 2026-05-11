import { TopBar } from '@/components/TopBar'
import { HOSPITALIZATIONS } from '@/routes'

export default function Account() {
  // TODO: configurações da conta. Formulário - Reaproveitar o form de doutor
  return (
    <TopBar>
      <TopBar.Back href={HOSPITALIZATIONS.PENDINGS} />
      <TopBar.Title>Minha Conta</TopBar.Title>
    </TopBar>
  )
}
