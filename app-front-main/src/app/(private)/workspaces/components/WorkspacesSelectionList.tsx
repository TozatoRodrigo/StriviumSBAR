import { useWorkspaces } from '@/hooks/queries/workspaces'
import { Stack } from '@mui/material'
import { WorkspaceCard } from './WorkspaceCard'
import { WorkspacesSelectionEmptyList } from './WorkspacesSelectionEmptyList'
import { useEffect, useMemo, useRef } from 'react'
import { ErrorState } from '@/components/ErrorState'
import { useRouter } from 'next/navigation'

type WorkspacesSelectionListProps = {
  canEvaluateOnboardingRedirect: boolean
  hasPendingInvites: boolean
}

export const WorkspacesSelectionList = ({
  canEvaluateOnboardingRedirect,
  hasPendingInvites,
}: WorkspacesSelectionListProps) => {
  const router = useRouter()
  const hasRedirectedToOnboarding = useRef(false)
  const { data, isLoading, isError, refetch } = useWorkspaces()

  const workspaces = useMemo(() => data?.data, [data?.data])

  useEffect(() => {
    if (hasRedirectedToOnboarding.current) return
    if (isLoading || isError || !workspaces) return
    if (!canEvaluateOnboardingRedirect || hasPendingInvites) return
    if (workspaces.length === 0) {
      hasRedirectedToOnboarding.current = true
      router.replace('/onboarding')
    }
  }, [canEvaluateOnboardingRedirect, hasPendingInvites, isError, isLoading, router, workspaces])

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
