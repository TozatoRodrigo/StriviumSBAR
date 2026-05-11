'use client'

import { Badge, Box, Stack, Tab, Tabs } from '@mui/material'
import { WorkspacesSelectionList } from './components/WorkspacesSelectionList'
import { OnlyAuthLayout } from '@/components/layouts/OnlyAuthLayout'
import { PropsWithChildren, SyntheticEvent, useState } from 'react'
import { useWorkspacesPendingInvitesCount } from '@/hooks/queries/workspacesUser'
import { WorkspacesInvitesList } from './components/WorkspacesInvitesList'

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

function a11yProps(index: number) {
  return {
    id: `tab-${index}`,
    'aria-controls': `tabpanel-${index}`,
  }
}

export default function Workspaces() {
  const [tab, setTab] = useState(0)

  const handleChange = (_: SyntheticEvent, newValue: number) => {
    setTab(newValue)
  }

  const { data: invites } = useWorkspacesPendingInvitesCount()

  return (
    <OnlyAuthLayout>
      <Stack sx={{ minHeight: '100%', flex: 1 }} className="bg-white">
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tab} onChange={handleChange} variant="fullWidth" aria-label="basic tabs example">
            <Tab label="Locais de trabalho" {...a11yProps(0)} />
            <Tab
              label={
                <Box display="flex" gap={2} alignItems="center">
                  Convites
                  {!!invites.count && (
                    <Badge badgeContent={invites.count} color="error" sx={{ transform: 'translateY(-2px)' }} />
                  )}
                </Box>
              }
              {...a11yProps(1)}
            />
          </Tabs>
        </Box>
        <CustomTabPanel value={tab} index={0}>
          <WorkspacesSelectionList />
        </CustomTabPanel>
        <CustomTabPanel value={tab} index={1}>
          <WorkspacesInvitesList />
        </CustomTabPanel>
      </Stack>
    </OnlyAuthLayout>
  )
}
