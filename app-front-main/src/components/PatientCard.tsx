'use client'

import { Button, Skeleton, Typography } from '@mui/material'

import { Chip, Stack, Card, CardContent } from '@mui/material'
import PersonOutlineIcon from '@mui/icons-material/PersonOutline'
import CalendarTodayIcon from '@mui/icons-material/CalendarToday'
import LocalHospitalIcon from '@mui/icons-material/LocalHospital'
import EditNoteIcon from '@mui/icons-material/EditNote'
import ChevronRightIcon from '@mui/icons-material/ChevronRight'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { format } from '@/lib/date'
import { joinFullname } from '@/lib/utils'

type PatientCardProps = {
  id: string
  patient: {
    first_name: string
    last_name: string
  }
  created_at: string
  sector: string
  reason: string
  place: string
  status: string
}

export const PatientCard = ({ patient, created_at, sector, reason, place, id, status }: PatientCardProps) => {
  const pathname = usePathname()
  const isExpired = status === 'TODO: verificar'
  const mainColor = isExpired ? '#FF0000' : '#4283F1'
  const name = joinFullname(patient.first_name, patient.last_name)
  return (
    <Card
      elevation={0}
      sx={{
        borderLeft: `1px solid ${mainColor}`,
        borderRadius: '8px',
      }}
    >
      <CardContent sx={{ p: 2 }}>
        <Stack direction="row" spacing={1} alignItems="center">
          <PersonOutlineIcon color={isExpired ? 'error' : 'primary'} />
          <Typography fontWeight={400} fontSize={16}>
            {name}
          </Typography>
        </Stack>

        <Stack direction="row" spacing={1} mt={1} alignItems="center">
          <CalendarTodayIcon fontSize="small" color="disabled" />
          <Typography variant="body2" color="text.secondary">
            Horário: {format(created_at, 'HH:mm')}
          </Typography>
          <LocalHospitalIcon fontSize="small" color="disabled" sx={{ ml: 2 }} />
          <Typography variant="body2" color="text.secondary">
            Setor: {sector}
          </Typography>
        </Stack>

        <Stack direction="row" spacing={1} mt={1} alignItems="flex-start">
          <EditNoteIcon fontSize="small" color="disabled" />
          <Typography variant="body2" color="text.secondary" noWrap sx={{ maxWidth: '90%' }}>
            Motivo: {reason}
          </Typography>
        </Stack>

        <Stack direction="row" justifyContent="space-between" alignItems="center" mt={1}>
          <Chip
            label={place}
            size="small"
            variant="outlined"
            sx={{
              bgcolor: '#e8f0fe',
              color: '#4285F4',
              borderColor: 'transparent',
              fontWeight: 500,
            }}
          />

          <Stack alignItems={'center'}>
            <Button
              className="text-[#64748B]"
              sx={{ fontSize: '12px' }}
              LinkComponent={Link}
              href={`/hospitalizations/detail?hospitalization_id=${id}&from=${pathname}`}
              endIcon={<ChevronRightIcon fontSize="inherit" />}
              size={'small'}
            >
              Visitar
            </Button>
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  )
}

function PatientCardSkeleton({ mainColor = '#ccc' }: { mainColor?: string }) {
  return (
    <Card
      elevation={0}
      sx={{
        borderLeft: `1px solid ${mainColor}`,
        borderRadius: '8px',
      }}
    >
      <CardContent sx={{ p: 2 }}>
        <Stack direction="row" spacing={1} alignItems="center">
          <PersonOutlineIcon color="disabled" />
          <Skeleton width="40%" height={24} />
        </Stack>

        <Stack direction="row" spacing={1} mt={1} alignItems="center">
          <CalendarTodayIcon fontSize="small" color="disabled" />
          <Skeleton width="20%" height={18} />
          <LocalHospitalIcon fontSize="small" color="disabled" sx={{ ml: 2 }} />
          <Skeleton width="25%" height={18} />
        </Stack>

        <Stack direction="row" spacing={1} mt={1} alignItems="flex-start">
          <EditNoteIcon fontSize="small" color="disabled" />
          <Skeleton width="90%" height={18} />
        </Stack>

        <Stack direction="row" justifyContent="space-between" alignItems="center" mt={1}>
          <Stack direction="row" spacing={1}>
            {[...Array(2)].map((_, index) => (
              <Skeleton key={index} variant="rounded" width={60} height={24} sx={{ borderRadius: '12px' }} />
            ))}
          </Stack>

          <Button
            disabled
            sx={{ fontSize: '12px', color: '#64748B' }}
            endIcon={<ChevronRightIcon fontSize="inherit" />}
            size="small"
          >
            Visitar
          </Button>
        </Stack>
      </CardContent>
    </Card>
  )
}

PatientCard.Skeleton = PatientCardSkeleton
