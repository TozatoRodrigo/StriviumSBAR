import { Box, SpeedDial, SpeedDialAction } from '@mui/material'
import SpeedDialIcon from '@mui/material/SpeedDialIcon'

import { useRouter } from 'next/navigation'
import { JSX, SyntheticEvent, useState } from 'react'

type SpeedDialCustomProps = {
  actions: {
    name: string
    icon: JSX.Element
    href: string
  }[]
}

export const SpeedDialCustom = ({ actions }: SpeedDialCustomProps) => {
  const nav = useRouter()
  const [open, setOpen] = useState(false)
  const handleOpen = (event: SyntheticEvent<object, Event>) => {
    if (event.type === 'click') setOpen(true)
  }
  const handleClose = (event: SyntheticEvent<object, Event>) => {
    if (['blur', 'click'].includes(event.type)) setOpen(false)
  }

  return (
    <SpeedDial
      FabProps={{ size: 'small' }}
      ariaLabel="Add items"
      sx={{ position: 'absolute', bottom: 65, right: 4 }}
      icon={<SpeedDialIcon />}
      onClose={handleClose}
      onOpen={handleOpen}
      open={open}
    >
      {actions.map(action => (
        <SpeedDialAction
          key={action.name}
          icon={
            <Box className="py-2.5 px-6 px flex items-center gap-2 bg-[#4283F1] rounded-full text-sm text-white hover:scale-105">
              {action.icon}
              <span>{action.name}</span>
            </Box>
          }
          onClick={() => nav.push(action.href)}
          slotProps={{
            fab: {
              disableRipple: true,
              disableFocusRipple: true,
              sx: {
                justifyContent: 'flex-end',
                background: 'transparent',
              },
            },
          }}
        />
      ))}
    </SpeedDial>
  )
}
