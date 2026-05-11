import { MouseEvent, useMemo, useState } from 'react'
import { Box, Typography, Card, CardContent, IconButton, Stack, Menu, MenuItem } from '@mui/material'
import MoreVert from '@mui/icons-material/MoreVert'
import { useWorkspacePendingInvites } from '@/hooks/queries/workspacesUser'
import { ErrorState } from '@/components/ErrorState'
import { EmptyState } from '@/components/EmptyState'
import { Skeleton } from '@mui/material'
import { InfiniteLoading } from '@/components/InfiniteLoading'

export const InvitesList = () => {
  const { data, isLoading, isError, isFetchingNextPage, refetch, fetchNextPage, hasNextPage } =
    useWorkspacePendingInvites()
  const invites = useMemo(() => data?.pages.flatMap(page => page.data), [data?.pages])
  const [anchorEl, setAnchorEl] = useState<Element | null>(null)
  const [, setSelectedId] = useState<string | null>(null)

  const handleOpenMenu = (event: MouseEvent<Element>, id: string | null) => {
    setAnchorEl(event.currentTarget)
    setSelectedId(id)
  }
  const handleCloseMenu = () => {
    setAnchorEl(null)
    setSelectedId(null)
  }

  if (isLoading) return <InviteCardSkeleton />
  if (isError || !invites) return <ErrorState onRetry={refetch} />
  if (!invites.length) return <EmptyState message={'Não há convites pendentes'} />

  return (
    <>
      <Stack spacing={2} mt={2}>
        {invites.map(invite => (
          <Card key={invite.id} variant="outlined">
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="start">
                <Box>
                  <Typography variant="subtitle1">{invite.email}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Papel: {invite.role.description}
                  </Typography>
                </Box>
                <IconButton hidden onClick={e => handleOpenMenu(e, invite.id)}>
                  <MoreVert />
                </IconButton>
              </Box>
            </CardContent>
          </Card>
        ))}
      </Stack>
      <InfiniteLoading
        fetchNextPage={fetchNextPage}
        hasNextPage={hasNextPage}
        isError={isError}
        isFetchingNextPage={isFetchingNextPage}
      />
      <Menu hidden anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleCloseMenu}>
        {/* TODO: implementar */}
        <MenuItem onClick={() => {}}>Cancelar</MenuItem>
      </Menu>
    </>
  )
}

export const InviteCardSkeleton = () => {
  return (
    <Card variant="outlined">
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="start">
          <Box>
            <Skeleton variant="text" width={160} height={24} />
            <Skeleton variant="text" width={120} height={20} />
          </Box>
          <IconButton disabled>
            <MoreVert />
          </IconButton>
        </Box>
      </CardContent>
    </Card>
  )
}
