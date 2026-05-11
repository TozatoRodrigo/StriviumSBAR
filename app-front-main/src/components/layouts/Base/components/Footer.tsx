import HistoryIcon from '@mui/icons-material/History'
import TaskAltIcon from '@mui/icons-material/TaskAlt'
import AccountCircle from '@mui/icons-material/AccountCircle'
import BusinessIcon from '@mui/icons-material/Business'

import { BottomNavigation, BottomNavigationAction } from '@mui/material'
import { useCallback, useEffect, useState } from 'react'
import { HOSPITALIZATIONS } from '@/routes'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useWorkspace } from '@/contexts/WorkspaceContext'

type Props = {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  actionHandler: (arg: any) => void
}

export const Footer = ({ actionHandler = () => {} }: Props) => {
  const pathname = usePathname()
  const [value, setValue] = useState(pathname)

  const refreshSelected = useCallback(() => setValue(pathname), [pathname])

  useEffect(refreshSelected)

  const {
    states: { isAuth },
  } = useWorkspace()

  return (
    <BottomNavigation
      showLabels
      value={value}
      onChange={(_, newValue) => {
        setValue(newValue)
      }}
    >
      {!isAuth && (
        <BottomNavigationAction
          label="Locais de trabalho"
          icon={<BusinessIcon />}
          component={Link}
          value={'/workspaces'}
          href={'/workspaces'}
        />
      )}
      {isAuth && (
        <BottomNavigationAction
          label="Pendentes"
          icon={<HistoryIcon />}
          component={Link}
          value={HOSPITALIZATIONS.PENDINGS}
          href={HOSPITALIZATIONS.PENDINGS}
        />
      )}
      {isAuth && (
        <BottomNavigationAction
          label="Concluídos"
          icon={<TaskAltIcon />}
          component={Link}
          value={HOSPITALIZATIONS.DONE}
          href={HOSPITALIZATIONS.DONE}
        />
      )}
      <BottomNavigationAction
        label="Perfil"
        icon={<AccountCircle />}
        onClick={() =>
          actionHandler({
            type: 'profile',
          })
        }
      />
    </BottomNavigation>
  )
}
