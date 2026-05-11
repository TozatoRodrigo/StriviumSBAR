'use client'

import Link from 'next/link'
import { useMemo } from 'react'
import { ChipProps, Divider, MenuItem, Select, Skeleton, Stack, Typography, Box, IconButton } from '@mui/material'

import MedicalInformationIcon from '@mui/icons-material/MedicalInformation'
import LabelIcon from '@mui/icons-material/Label'
import LocationOnIcon from '@mui/icons-material/LocationOn'
import ApartmentIcon from '@mui/icons-material/Apartment'
import EditIcon from '@mui/icons-material/Edit'

import { useTranslation } from 'react-i18next'
import { joinFullname, withCallbackRoute } from '@/lib/utils'
import { HospitalizationStatus, useHospitalizations } from '@/hooks/queries/hospitalizations'
import { useRouter, usePathname, useSearchParams } from 'next/navigation'
import { format } from '@/lib/date'

type Hospitalization = {
  id: string
  number: string
  status: HospitalizationStatus
  sector: string
  reason: string
  place: string
  patient: {
    id: string
    first_name: string
    last_name: string
  }
}

type DetailHeaderProps = {
  hospitalization: Hospitalization
}

export const DetailHeader = ({
  hospitalization: { id, patient, status, number, sector, reason, place },
}: DetailHeaderProps) => {
  const name = joinFullname(patient.first_name, patient.last_name)
  const { t } = useTranslation()
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()

  const { data } = useHospitalizations({
    params: { patient_id: patient.id, limit: 100, search: '' },
    options: { enabled: !!patient.id },
  })
  const hospitalizations = useMemo(() => data?.pages.flatMap(page => page.data) ?? [], [data?.pages])

  const statusColor: Record<HospitalizationStatus, ChipProps['color']> = {
    active: 'success',
    deceased: 'warning',
    discharged: 'error',
  } as const

  const details = [
    { Icon: LabelIcon, title: 'Situação', label: t(status), color: statusColor[status] },
    { Icon: MedicalInformationIcon, title: 'Número', label: number, color: 'text.secondary' },
    { Icon: LocationOnIcon, title: 'Local', label: place, color: 'text.secondary' },
    { Icon: ApartmentIcon, title: 'Setor', label: sector, color: 'text.secondary' },
    { Icon: EditIcon, title: 'Motivo', label: reason, color: 'text.secondary' },
  ]

  return (
    <Stack className="p-4" gap={1.5}>
      <div className="flex justify-between items-center">
        <Typography variant="h6" fontWeight={600}>
          {name}
        </Typography>
      </div>
      {hospitalizations.length > 0 && (
        <Select
          size="small"
          value={id}
          onChange={e => router.push(`/hospitalizations/detail?hospitalization_id=${e.target.value}`)}
        >
          {hospitalizations.map(item => (
            <MenuItem key={item.id} value={item.id}>
              Internação - {format(item.created_at, 'dd/MM/yyyy')}
            </MenuItem>
          ))}
        </Select>
      )}
      <Divider>
        <Typography component="span" fontWeight={500} mr={1}>
          {' '}
          Dados da internação
        </Typography>
        <IconButton
          component={Link}
          href={withCallbackRoute(
            `/hospitalizations/edit?hospitalization_id=${id}`,
            `${pathname}?${searchParams.toString()}`
          )}
        >
          <EditIcon />
        </IconButton>
      </Divider>

      <Stack spacing={1}>
        {details.map(({ Icon, title, label, color }, index) => (
          <Box key={index} sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Icon sx={{ color: '#64748B' }} fontSize="small" />
            <Typography component="span" color={color} fontSize={14}>
              <Typography component="span" sx={{ fontWeight: 500, color: 'text.primary' }}>
                {title}:{' '}
              </Typography>
              {label}
            </Typography>
          </Box>
        ))}
      </Stack>
      <Divider />
    </Stack>
  )
}

export const DetailHeaderSkeleton = () => {
  return (
    <Stack className="p-4" gap={1.5}>
      <div className="flex justify-between items-center">
        <Skeleton variant="text" width={200} />
      </div>
      <Skeleton variant="rounded" height={40} />

      <Divider>
        <Typography component="span" fontWeight={500} mr={1}>
          <Skeleton variant="text" width={150} />
        </Typography>
      </Divider>

      <Stack spacing={1}>
        {[LabelIcon, MedicalInformationIcon, LocationOnIcon, ApartmentIcon, EditIcon].map((Icon, index) => (
          <Box key={index} sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Icon sx={{ color: '#64748B' }} fontSize="small" />

            <Skeleton variant="text" width="40%" />
          </Box>
        ))}
      </Stack>
      <Divider />
    </Stack>
  )
}

DetailHeader.Skeleton = DetailHeaderSkeleton
