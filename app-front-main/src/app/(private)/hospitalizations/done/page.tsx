'use client'

import { ErrorState } from '@/components/ErrorState'
import { HospitalizationInfo, Hospitalizations } from '@/components/Hospitalizations'
import { InfiniteLoading } from '@/components/InfiniteLoading'
import { useDone } from '@/hooks/queries/hospitalizations'
import { Stack } from '@mui/material'
import { useMemo } from 'react'

export default function Done() {
  const { data, fetchNextPage, hasNextPage, isLoading, isFetchingNextPage, isError, refetch } = useDone(5)

  const hospitalizations = useMemo<HospitalizationInfo[]>(
    () => data?.pages.flatMap(page => page.data) ?? [],
    [data?.pages]
  )
  if (isLoading) return <Hospitalizations.Skeleton />
  if (isError || !hospitalizations) return <ErrorState onRetry={refetch} />

  return (
    <Stack>
      <div className="grid gap-2">
        <Hospitalizations hospitalizations={hospitalizations} />
        <InfiniteLoading
          fetchNextPage={fetchNextPage}
          hasNextPage={hasNextPage}
          isError={isError}
          isFetchingNextPage={isFetchingNextPage}
        />
      </div>
    </Stack>
  )
}
