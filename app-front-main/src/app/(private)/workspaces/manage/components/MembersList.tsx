import { useMemo } from 'react'
import { Stack } from '@mui/material'
import { useWorkspaceUsers } from '@/hooks/queries/workspacesUser'
import { ErrorState } from '@/components/ErrorState'
import { EmptyState } from '@/components/EmptyState'
import { InfiniteLoading } from '@/components/InfiniteLoading'
import { MemberCard } from './MemberCard'

type MembersListProps = {
  search?: string
}

export const MembersList = ({ search }: MembersListProps) => {
  const { data, fetchNextPage, hasNextPage, isLoading, isFetchingNextPage, isError, refetch } = useWorkspaceUsers({
    params: { limit: 5, search },
  })

  const members = useMemo(() => data?.pages.flatMap(page => page.data), [data?.pages])

  if (isLoading) return <MembersListSkeleton />
  if (isError || !members) return <ErrorState onRetry={refetch} />
  if (!members.length)
    return <EmptyState message={search ? 'Membro não localizado!' : 'Você ainda não possui membros cadastrados'} />

  return (
    <>
      <Stack spacing={2} mt={2}>
        {members.map(member => (
          <MemberCard key={member.id} {...member} />
        ))}
        <InfiniteLoading
          fetchNextPage={fetchNextPage}
          hasNextPage={hasNextPage}
          isError={isError}
          isFetchingNextPage={isFetchingNextPage}
        />
      </Stack>
    </>
  )
}

const MembersListSkeleton = () => {
  const placeholders = Array.from({ length: 1 })

  return (
    <Stack spacing={2} mt={2}>
      {placeholders.map((_, index) => (
        <MemberCard.Skeleton key={index} />
      ))}
    </Stack>
  )
}

MembersList.Skeleton = MembersListSkeleton
