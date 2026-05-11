import { useHospitalizations } from '@/hooks/queries/hospitalizations'
import { Stack, Typography } from '@mui/material'
import { HospitalizationCard } from './HospitalizationCard'
import { useMemo } from 'react'
import { InfiniteLoading } from '@/components/InfiniteLoading'
import { ErrorState } from '@/components/ErrorState'
import { EmptyState } from '@/components/EmptyState'

type HospitalizationListProps = {
  search?: string
}

export const HospitalizationList = ({ search = '' }: HospitalizationListProps) => {
  const { data, fetchNextPage, hasNextPage, isLoading, isFetchingNextPage, isError, refetch } = useHospitalizations({
    params: { search, limit: 5 },
    options: { keyword: 'hospitalizations-page' },
  })

  const hospitalizations = useMemo(() => data?.pages.flatMap(page => page.data), [data?.pages])

  if (isLoading) return <HospitalizationListSkeleton />
  if (isError || !hospitalizations) return <ErrorState onRetry={refetch} />
  if (!hospitalizations.length)
    return (
      <EmptyState message={search ? 'Internação não localizada!' : 'Você ainda não possui internações cadastrados'} />
    )

  return (
    <Stack gap={2}>
      <Typography className="font-normal text-sm text-[#64748B]">Internações:</Typography>

      <Stack gap={1} display="grid">
        {hospitalizations.map(hospitalization => (
          <HospitalizationCard key={hospitalization.id} {...hospitalization} />
        ))}
        <InfiniteLoading
          fetchNextPage={fetchNextPage}
          hasNextPage={hasNextPage}
          isError={isError}
          isFetchingNextPage={isFetchingNextPage}
        />
      </Stack>
    </Stack>
  )
}

const HospitalizationListSkeleton = () => {
  return (
    <Stack gap={2}>
      <Typography className="font-normal text-sm text-[#64748B]">Internações:</Typography>

      <Stack gap={1}>
        {Array.from({ length: 3 }).map((_, index) => (
          <HospitalizationCard.Skeleton key={index} />
        ))}
      </Stack>
    </Stack>
  )
}

HospitalizationList.Skeleton = HospitalizationListSkeleton
