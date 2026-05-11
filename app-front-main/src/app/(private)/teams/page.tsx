'use client'
import { TopBar } from '@/components/TopBar'
import { useDebounce } from '@/hooks/useDebounce'
import { HOSPITALIZATIONS } from '@/routes'
import { Box, IconButton, InputAdornment, Stack, TextField, useTheme } from '@mui/material'
import { useState } from 'react'
import SearchIcon from '@mui/icons-material/Search'
import Link from 'next/link'
import AddIcon from '@mui/icons-material/Add'
import { TeamList } from './components/TeamList'

export default function Teams() {
  const [search, setSearch] = useState('')
  const searchDebounced = useDebounce(search, 500)
  const { palette } = useTheme()

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
      <TopBar>
        <TopBar.Back href={HOSPITALIZATIONS.PENDINGS} />
        <TopBar.Title>Equipes</TopBar.Title>
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
            placeholder="Buscar equipe"
          />
          <IconButton
            LinkComponent={Link}
            href="/teams/create"
            aria-label="Adicionar equipe"
            title="Adicionar equipe"
            size="large"
            disableRipple
            sx={{ background: palette.primary.main, color: 'white' }}
          >
            <AddIcon />
          </IconButton>
        </Stack>

        <TeamList search={searchDebounced} />
      </Stack>
    </Box>
  )
}
