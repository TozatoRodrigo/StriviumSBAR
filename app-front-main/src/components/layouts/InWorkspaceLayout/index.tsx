'use client'

import { PropsWithChildren } from 'react'
import AddIcon from '@mui/icons-material/Add'
import { Header } from './components/Header'

import { SpeedDialCustom } from '@/components/SpeedDialCustom'
import { Base } from '../Base'
import { useWorkspace } from '@/contexts/WorkspaceContext'

export const InWorkspaceLayout = ({ children }: PropsWithChildren) => {
  const {
    info: workspaceInfo,
    states: { isRole },
  } = useWorkspace()

  const actions = [
    { icon: <AddIcon />, name: 'Internação', href: '/hospitalizations/create', canShow: true },
    {
      icon: <AddIcon />,
      name: 'Membro',
      href: `/workspaces/manage?workspace_id=${workspaceInfo?.tenant.id}&modal=invite`,
      canShow: isRole.admin,
    },
    { icon: <AddIcon />, name: 'Equipe', href: '/teams/create', canShow: isRole.admin },
  ]

  return (
    <Base header={<Header />} speedDial={<SpeedDialCustom actions={actions} />}>
      {children}
    </Base>
  )
}
