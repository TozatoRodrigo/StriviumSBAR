import { useDoctors } from '@/hooks/queries/doctors'
import { Stack, Typography } from '@mui/material'
import { DoctorCard } from './DoctorCard'
import { useMemo } from 'react'
import { ErrorState } from '@/components/ErrorState'
import { EmptyState } from '@/components/EmptyState'

type DoctorListProps = {
  search?: string
}

export const DoctorList = ({ search = '' }: DoctorListProps) => {
  const { data, isLoading, isError, refetch } = useDoctors({ params: { search }, options: { keyword: 'doctors-page' } })

  const doctors = useMemo(() => data?.data, [data?.data])

  if (isLoading) return <DoctorListSkeleton />
  if (isError || !doctors) return <ErrorState onRetry={refetch} />
  if (!doctors.length)
    return <EmptyState message={search ? 'Médico não localizado!' : 'Você ainda não possui médicos cadastrados'} />

  return (
    <Stack gap={2}>
      <Typography className="font-normal text-sm text-[#64748B]">Médicos:</Typography>

      <Stack gap={1}>
        {doctors?.map(doctor => (
          <DoctorCard key={doctor.id} {...doctor} />
        ))}
      </Stack>
    </Stack>
  )
}

const DoctorListSkeleton = () => {
  return (
    <Stack gap={2}>
      <Typography className="font-normal text-sm text-[#64748B]">Médicos:</Typography>

      <Stack gap={1}>
        {Array.from({ length: 3 }).map((_, index) => (
          <DoctorCard.Skeleton key={index} />
        ))}
      </Stack>
    </Stack>
  )
}

DoctorList.Skeleton = DoctorListSkeleton
