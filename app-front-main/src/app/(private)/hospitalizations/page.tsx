'use client'
import { TopBar } from '@/components/TopBar'
import { useDebounce } from '@/hooks/useDebounce'
import { HOSPITALIZATIONS } from '@/routes'
import { Box, IconButton, InputAdornment, Stack, TextField, useTheme } from '@mui/material'
import { useState } from 'react'
import SearchIcon from '@mui/icons-material/Search'
import Link from 'next/link'
import AddIcon from '@mui/icons-material/Add'
import { HospitalizationList } from './components/HospitalizationList'

export default function Hospitalizations() {
  const [search, setSearch] = useState('')
  const searchDebounced = useDebounce(search, 500)
  const { palette } = useTheme()

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
      <TopBar>
        <TopBar.Back href={HOSPITALIZATIONS.PENDINGS} />
        <TopBar.Title>Internações</TopBar.Title>
      </TopBar>

      <Stack className="p-4" flex={1} gap={2}>
        <Stack gap={2} flexDirection="row" alignItems="center">
          <TextField
            autoFocus
            value={search}
            sx={{ flex: 1 }}
            onChange={event => setSearch(event.target.value)}
            slotProps={{
              input: {
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
                sx: {
                  borderRadius: '999px',
                },
              },
            }}
            placeholder="Buscar por internação"
          />
          <IconButton
            LinkComponent={Link}
            href="/hospitalizations/create"
            aria-label="Adicionar internação"
            title="Adicionar internação"
            size="large"
            disableRipple
            sx={{ background: palette.primary.main, color: 'white' }}
          >
            <AddIcon />
          </IconButton>
        </Stack>

        <HospitalizationList search={searchDebounced} />
      </Stack>
    </Box>
  )
}
