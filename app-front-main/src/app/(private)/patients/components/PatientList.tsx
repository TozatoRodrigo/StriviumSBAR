import { usePatients } from '@/hooks/queries/patients'
import { Stack, Typography } from '@mui/material'
import { PatientCard } from './PatientCard'
import { useMemo } from 'react'
import { ErrorState } from '@/components/ErrorState'
import { EmptyState } from '@/components/EmptyState'

type PatientListProps = {
  search?: string
}

export const PatientList = ({ search = '' }: PatientListProps) => {
  const { data, isLoading, isError, refetch } = usePatients({
    params: { search },
    options: { keyword: 'patients-page' },
  })

  const patients = useMemo(() => data?.data, [data?.data])

  if (isLoading) return <PatientListSkeleton />
  if (isError || !patients) return <ErrorState onRetry={refetch} />
  if (!patients.length)
    return <EmptyState message={search ? 'Paciente não localizado!' : 'Você ainda não possui pacientes cadastrados'} />

  return (
    <Stack gap={2}>
      <Typography className="font-normal text-sm text-[#64748B]">Pacientes:</Typography>

      <Stack gap={1}>
        {patients?.map(patient => (
          <PatientCard key={patient.id} {...patient} />
        ))}
      </Stack>
    </Stack>
  )
}

const PatientListSkeleton = () => {
  return (
    <Stack gap={2}>
      <Typography className="font-normal text-sm text-[#64748B]">Pacientes:</Typography>

      <Stack gap={1}>
        {Array.from({ length: 3 }).map((_, index) => (
          <PatientCard.Skeleton key={index} />
        ))}
      </Stack>
    </Stack>
  )
}

PatientList.Skeleton = PatientListSkeleton
