import { Stack, Typography } from '@mui/material'
import { PatientCard } from './PatientCard'
import Image from 'next/image'

export type HospitalizationInfo = {
  id: string
  patient: {
    first_name: string
    last_name: string
  }
  created_at: string
  sector: string
  reason: string
  status: string
  place: string
}

type HospitalizationsProps = {
  hospitalizations: HospitalizationInfo[]
}

const EmptyList = () => {
  return (
    <Stack gap={2} pt={4}>
      <Image
        className="self-center"
        src="/empty_hospitalizations.png"
        alt="Lista vazia"
        unoptimized
        width={200}
        height={200}
      />
      <Stack alignItems="center">
        <Typography className="font-normal text-[#020617] text-xl">Sem internações</Typography>
      </Stack>
    </Stack>
  )
}

export const Hospitalizations = ({ hospitalizations }: HospitalizationsProps) => {
  if (!hospitalizations.length) {
    return <EmptyList />
  }

  return hospitalizations.map(item => <PatientCard key={item.id} {...item} />)
}

const HospitalizationsSkeleton = () => {
  return (
    <Stack gap={1}>
      {Array.from({ length: 4 }).map((_, index) => (
        <PatientCard.Skeleton key={index} />
      ))}
    </Stack>
  )
}

Hospitalizations.Skeleton = HospitalizationsSkeleton
