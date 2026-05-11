'use client'

// import { useWorkspacesParams } from '@/hooks/queryParams/workspaces'

import React, { PropsWithChildren, useState } from 'react'
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Tabs,
  Tab,
  Stack,
  TextField,
  InputAdornment,
  Skeleton,
} from '@mui/material'
import { PersonAdd } from '@mui/icons-material'
import { InviteDialog } from './components/InviteDialog'
import { MembersList } from './components/MembersList'
import { InvitesList } from './components/InvitesList'
import { TopBar } from '@/components/TopBar'
import { HOSPITALIZATIONS } from '@/routes'
import { useDebounce } from '@/hooks/useDebounce'
import SearchIcon from '@mui/icons-material/Search'
import { useWorkspacesParams } from '@/hooks/queryParams/workspaces'
import { useWorkspace } from '@/hooks/queries/workspaces'

type TabPanelProps = {
  index: number
  value: number
}

function CustomTabPanel({ children, value, index, ...other }: PropsWithChildren<TabPanelProps>) {
  return (
    <div role="tabpanel" hidden={value !== index} id={`tabpanel-${index}`} aria-labelledby={`tab-${index}`} {...other}>
      {value === index && <Box>{children}</Box>}
    </div>
  )
}

function Title() {
  const { workspace_id } = useWorkspacesParams()
  const { data: workspace, isLoading, isError } = useWorkspace(workspace_id!)

  if (isLoading) return <Skeleton variant="text" width="40%" height={32} />
  if (isError || !workspace) return null

  return <Typography variant="h6">{workspace?.name}</Typography>
}

export default function WorkspaceManager() {
  const { modal } = useWorkspacesParams()

  const [dialogOpen, setDialogOpen] = useState(modal === 'invite')
  const [tab, setTab] = useState(0)

  const [search, setSearch] = useState<string | undefined>()
  const searchDebounced = useDebounce(search, 500)

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
      <TopBar>
        <TopBar.Back href={HOSPITALIZATIONS.PENDINGS} />
        <TopBar.Title>Gerenciar local de trabalho</TopBar.Title>
      </TopBar>

      <Stack className="p-4" flex={1} gap={2}>
        <Title />
        <Card>
          <CardContent>
            <Box display="flex" justifyContent="space-between" alignItems="center">
              <Tabs value={tab} onChange={(e, v) => setTab(v)} variant="fullWidth">
                <Tab label="Membros" />
                <Tab label="Convites" />
              </Tabs>
              {tab === 0 && (
                <Button size="small" variant="contained" startIcon={<PersonAdd />} onClick={() => setDialogOpen(true)}>
                  Convidar
                </Button>
              )}
            </Box>

            <CustomTabPanel value={tab} index={0}>
              <Stack flexDirection="column" mt={2}>
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
                  placeholder="Buscar"
                />
                <MembersList search={searchDebounced} />
              </Stack>
            </CustomTabPanel>
            <CustomTabPanel value={tab} index={1}>
              <InvitesList />
            </CustomTabPanel>
          </CardContent>
        </Card>
      </Stack>
      {dialogOpen && <InviteDialog open={dialogOpen} onClose={() => setDialogOpen(false)} />}
    </Box>
  )
}
