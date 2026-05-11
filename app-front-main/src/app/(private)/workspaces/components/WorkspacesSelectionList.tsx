import { useWorkspaces } from '@/hooks/queries/workspaces'
import { Stack } from '@mui/material'
import { WorkspaceCard } from './WorkspaceCard'
import { WorkspacesSelectionEmptyList } from './WorkspacesSelectionEmptyList'
import { useMemo } from 'react'
import { ErrorState } from '@/components/ErrorState'

export const WorkspacesSelectionList = () => {
  const { data, isLoading, isError, refetch } = useWorkspaces()

  const workspaces = useMemo(() => data?.data, [data?.data])

  if (isLoading) return <WorkspacesSelectionListSkeleton />
  if (isError || !workspaces) return <ErrorState onRetry={refetch} />
  if (!workspaces.length) return <WorkspacesSelectionEmptyList />

  return (
    <Stack className="p-4" flex={1} gap={2}>
      {workspaces.map(workspace => (
        <WorkspaceCard key={workspace.id} {...workspace} />
      ))}
    </Stack>
  )
}

export const WorkspacesSelectionListSkeleton = () => {
  const placeholders = Array.from({ length: 3 })

  return (
    <Stack className="p-4" flex={1} gap={2}>
      {placeholders.map((_, index) => (
        <WorkspaceCard.Skeleton key={index} />
      ))}
    </Stack>
  )
}

WorkspacesSelectionList.Skeleton = WorkspacesSelectionListSkeleton
