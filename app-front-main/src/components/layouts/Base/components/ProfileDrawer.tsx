'use client'

import {
  Button,
  Divider,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
} from '@mui/material'
import { RefObject } from 'react'
import MedicalServicesIcon from '@mui/icons-material/MedicalServices'
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft'

import PersonIcon from '@mui/icons-material/Person'
import CreditCardIcon from '@mui/icons-material/CreditCard'
import GroupsIcon from '@mui/icons-material/Groups'
import MedicalInformationIcon from '@mui/icons-material/MedicalInformation'
import SettingsIcon from '@mui/icons-material/Settings'
import WorkspacePremiumIcon from '@mui/icons-material/WorkspacePremium'
import PeopleOutlinedIcon from '@mui/icons-material/PeopleOutlined'
import BusinessIcon from '@mui/icons-material/Business'
import Link from 'next/link'
import { useAuth } from '@/contexts/AuthContext'
import { useWorkspace } from '@/contexts/WorkspaceContext'

const DrawerHeader = ({ children }: { children?: React.ReactNode }) => (
  <div className="flex items-center justify-start px-2 py-0 min-h-[64px]">{children}</div>
)

type ProfileDrawerProps = {
  open: boolean
  onClose: VoidFunction
  containerRef: RefObject<HTMLDivElement | null>
}

export const ProfileDrawer = ({ open, onClose, containerRef }: ProfileDrawerProps) => {
  const { logout } = useAuth()
  const {
    states: { isAuth, isRole },
    info: workspaceInfo,
  } = useWorkspace()

  const profileOptions = [
    {
      icon: <PersonIcon />,
      label: 'Minha conta',
      href: '/account',
      group: 'user',
      canShow: false /* TODO[v1]: enable */,
    },
    {
      icon: <CreditCardIcon />,
      label: 'Minhas assinaturas',
      href: '/subscriptions',
      group: 'user',
      canShow: false /* TODO[v1]: enable */,
    },
    {
      icon: <BusinessIcon />,
      label: 'Gerenciar local',
      href: `/workspaces/manage?workspace_id=${workspaceInfo?.tenant.id}`,
      group: 'manager',
      canShow: isRole.admin,
    },
    { icon: <GroupsIcon />, label: 'Equipes', href: '/teams', group: 'manager', canShow: isAuth },
    {
      icon: <MedicalServicesIcon />,
      label: 'Médicos',
      href: '/doctors',
      group: 'manager',
      canShow: false /* TODO[v1]: verificar necessidade dessa página */,
    },
    { icon: <PeopleOutlinedIcon />, label: 'Pacientes', href: '/patients', group: 'manager', canShow: isAuth },
    {
      icon: <MedicalInformationIcon />,
      label: 'Internações',
      href: '/hospitalizations',
      group: 'manager',
      canShow: isAuth,
    },
    {
      icon: <SettingsIcon />,
      label: 'Configurações',
      href: '/settings',
      group: 'settings',
      canShow: false /* TODO[v1]: enable */,
    },
    {
      icon: <WorkspacePremiumIcon />,
      label: 'Planos',
      href: '/plans',
      group: 'system',
      canShow: false /* TODO[v1]: enable */,
    },
  ]

  return (
    <Drawer
      open={open}
      onClose={onClose}
      anchor="right"
      container={containerRef?.current}
      ModalProps={{
        container: containerRef?.current,
      }}
      sx={{
        position: 'absolute',
        '& .MuiDrawer-paper': {
          position: 'absolute',
          minWidth: '50%',
          transition: 'transform 500ms ease-in-out !important',
        },
        '.MuiBackdrop-root': {
          position: 'absolute',
        },
      }}
    >
      <DrawerHeader>
        <IconButton onClick={onClose}>{<ChevronLeftIcon />}</IconButton>
        <Typography variant="h6">Perfil</Typography>
      </DrawerHeader>
      <Divider />
      <List className="flex-1">
        {profileOptions
          .filter(({ canShow }) => canShow)
          .map(({ label, icon, href, group }, index, arr) => (
            <div key={label}>
              <ListItem disablePadding>
                <ListItemButton LinkComponent={Link} href={href}>
                  <ListItemIcon>{icon}</ListItemIcon>
                  <ListItemText primary={label} />
                </ListItemButton>
              </ListItem>
              {index + 1 < arr.length && group != arr[index + 1].group && <Divider />}
            </div>
          ))}
      </List>

      <Button className="m-4" color="error" onClick={logout}>
        Sair
      </Button>
    </Drawer>
  )
}
