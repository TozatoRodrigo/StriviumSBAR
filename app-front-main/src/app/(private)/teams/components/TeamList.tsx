import { useTeams } from '@/hooks/queries/teams'
import { TeamCard } from './TeamCard'
import { useMemo } from 'react'
import { ErrorState } from '@/components/ErrorState'
import { EmptyState } from '@/components/EmptyState'
import { InfiniteLoading } from '@/components/InfiniteLoading'
import { Stack, Typography } from '@mui/material'

type TeamListProps = {
  search: string
}

export const TeamList = ({ search }: TeamListProps) => {
  const { data, isLoading, isError, refetch, fetchNextPage, hasNextPage, isFetchingNextPage } = useTeams({
    params: { search, limit: 5 },
    options: { keyword: 'teams-page', enabled: true },
  })

  const teams = useMemo(() => data?.pages.flatMap(page => page.data) ?? [], [data?.pages])

  if (isLoading) return <TeamListSkeleton />
  if (isError || !teams) return <ErrorState onRetry={refetch} />
  if (!teams.length)
    return <EmptyState message={search ? 'Equipe não localizada!' : 'Você ainda não possui equipes cadastradas'} />

  return (
    <>
      <Stack gap={2}>
        <Typography className="font-normal text-sm text-[#64748B]">Equipes:</Typography>

        <Stack gap={1}>
          {teams.map(team => (
            <TeamCard key={team.id} {...team} />
          ))}
        </Stack>
      </Stack>
      <InfiniteLoading
        fetchNextPage={fetchNextPage}
        hasNextPage={hasNextPage}
        isError={isError}
        isFetchingNextPage={isFetchingNextPage}
      />
    </>
  )
}

const TeamListSkeleton = () => {
  return (
    <Stack gap={2}>
      <Typography className="font-normal text-sm text-[#64748B]">Equipes:</Typography>

      <Stack gap={1}>
        {Array.from({ length: 3 }).map((_, index) => (
          <TeamCard.Skeleton key={index} />
        ))}
      </Stack>
    </Stack>
  )
}

TeamList.Skeleton = TeamListSkeleton
