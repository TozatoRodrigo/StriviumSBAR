'use client'

import { PropsWithChildren } from 'react'
import AddIcon from '@mui/icons-material/Add'

import { SpeedDialCustom } from '@/components/SpeedDialCustom'
import { Base } from '../Base'
import { withCallbackRoute } from '@/lib/utils'
import { Header } from './components/Header'

const actions = [{ icon: <AddIcon />, name: 'Cadastrar local', href: withCallbackRoute('/workspaces/create', '') }]

export const OnlyAuthLayout = ({ children }: PropsWithChildren) => {
  return (
    <Base header={<Header />} speedDial={<SpeedDialCustom actions={actions} />}>
      {children}
    </Base>
  )
}
