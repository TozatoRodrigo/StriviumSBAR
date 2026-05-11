'use client'

import { MouseEvent, PropsWithChildren, useEffect, useState } from 'react'
import { IconButton, Menu } from '@mui/material'
import MoreVertIcon from '@mui/icons-material/MoreVert'

interface MenuOptionsProps {
  anchorEl: HTMLElement | null
  onOpen: (e: MouseEvent<HTMLElement>) => void
  onClose: () => void
  defaultOpen?: boolean
}

export const MenuOptions = ({
  children,
  anchorEl,
  onOpen,
  onClose,
  defaultOpen = false,
}: PropsWithChildren<MenuOptionsProps>) => {
  const [initialOpen, setInitialOpen] = useState(defaultOpen)
  const open = Boolean(anchorEl) || initialOpen

  useEffect(() => {
    if (defaultOpen && !anchorEl) {
      const btn = document.getElementById('menu-options-btn') as HTMLElement
      if (btn) {
        onOpen({ currentTarget: btn } as MouseEvent<HTMLElement>)
      }
      setInitialOpen(false)
    }
  }, [defaultOpen, anchorEl, onOpen])

  return (
    <div>
      <IconButton
        id="menu-options-btn"
        size="small"
        aria-controls={open ? 'options-menu' : undefined}
        aria-haspopup="true"
        aria-expanded={open ? 'true' : undefined}
        onClick={onOpen}
      >
        <MoreVertIcon fontSize="small" />
      </IconButton>

      <Menu
        id="options-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={onClose}
        slotProps={{
          paper: {
            elevation: 1,
            style: { width: '20ch' },
          },
        }}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
      >
        {children}
      </Menu>
    </div>
  )
}

export const useMenuOptions = () => {
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null)

  const handleOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }

  const handleClose = () => {
    setAnchorEl(null)
  }
  return { anchorEl, handleClose, handleOpen }
}

MenuOptions.useMenuOptions = useMenuOptions
