'use client'

import { useMemo } from 'react'
import { MenuItem, Skeleton, Typography, Box, Card, CardContent, Chip, ChipOwnProps, Stack } from '@mui/material'
import { alpha } from '@mui/material/styles'

import EditIcon from '@mui/icons-material/Edit'

import { TimelineItem, TimelineSeparator, TimelineConnector, TimelineContent, TimelineDot } from '@mui/lab'

import { format } from '@/lib/date'
import { MediaList } from './MediaList'
import { MenuOptions } from '@/components/MenuOptions'
import { joinFullname } from '@/lib/utils'
import { EvolutionHttpResponse, EvolutionSbar } from '@/hooks/queries/evolutions'
import { useRouter } from 'next/navigation'
import { useWorkspace } from '@/contexts/WorkspaceContext'
import { useAuth } from '@/contexts/AuthContext'
import { memberTypeLabels } from '@/constants/memberTypes'

type EvolutionProps = { isLatest: boolean; evolution: EvolutionHttpResponse }

const colorMap: { [key: string]: Exclude<ChipOwnProps['color'], undefined | 'default'> } = {
  [memberTypeLabels.doctor]: 'primary',
  [memberTypeLabels.nurse]: 'success',
  [memberTypeLabels.physiotherapist]: 'info',
  [memberTypeLabels.nutritionist]: 'warning',
  [memberTypeLabels.psychologist]: 'secondary',
  [memberTypeLabels.administrative_assistant]: 'info',
  [memberTypeLabels.speech_therapist]: 'primary',
  [memberTypeLabels.dentist]: 'error',
  [memberTypeLabels.social_worker]: 'success',
  [memberTypeLabels.radiologist]: 'info',
  [memberTypeLabels.occupational_therapist]: 'warning',
}

export const Evolution = ({
  evolution: { hospitalization_id, id, created_at, user, description, medias, sbar },
  isLatest,
}: EvolutionProps) => {
  const nav = useRouter()
  const { anchorEl, handleClose, handleOpen } = MenuOptions.useMenuOptions()
  const name = joinFullname(user.first_name, user.last_name)

  const {
    states: { isRole },
  } = useWorkspace()

  const { info } = useAuth()

  const chipColor = useMemo(() => (user.member_type ? colorMap[user.member_type] : undefined), [user.member_type])

  return (
    <TimelineItem>
      <TimelineSeparator>
        <TimelineDot
          color="primary"
          variant={isLatest ? 'filled' : 'outlined'}
          sx={{
            position: 'relative',
            '.MuiTimelineDot-filled&:before': {
              content: "''",
              position: 'absolute',
              border: '2px solid #1976d2',
              padding: '8px',
              borderRadius: '100%',
              transform: 'translate(-50%, -50%)',
            },
          }}
        />
        <TimelineConnector sx={{ bgcolor: 'primary.main' }} />
      </TimelineSeparator>
      {/* TODO: futuramente, agrupar por ano */}
      <TimelineContent>
        <Card elevation={0} sx={{ borderRadius: 2, p: 2 }}>
          <Box display="flex" justifyContent="space-between" alignItems="start">
            <Box>
              <Typography fontSize={12} fontWeight={700} sx={{ color: '#64748B' }}>
                {format(created_at, 'dd MMM')}
              </Typography>
            </Box>
            <Box textAlign="right" sx={{ display: 'flex' }} alignItems="center" gap={1}>
              <Typography fontSize={12} fontWeight={700} sx={{ color: '#64748B' }}>
                {format(created_at, 'HH:mm')}
              </Typography>
              {(isRole.admin || user.id === info?.id) && (
                <MenuOptions anchorEl={anchorEl} onOpen={handleOpen} onClose={handleClose}>
                  <MenuItem
                    onClick={() =>
                      nav.push(
                        `/hospitalizations/evolutions/edit?hospitalization_id=${hospitalization_id}&evolution_id=${id}`
                      )
                    }
                  >
                    <EditIcon fontSize="small" sx={{ color: '#49454F' }} />
                    <span className="ml-2">Editar</span>
                  </MenuItem>
                </MenuOptions>
              )}
            </Box>
          </Box>

          <CardContent sx={{ px: 0, pt: 0.5 }}>
            <Typography color="primary" fontWeight={600} component="div">
              {name}{' '}
              {user.member_type && (
                <Chip
                  label={user.member_type}
                  color={chipColor}
                  sx={theme => ({
                    backgroundColor: chipColor && alpha(theme.palette[chipColor].main, 0.2),
                    color: chipColor && theme.palette[chipColor].main,
                  })}
                  size="small"
                />
              )}
            </Typography>
            {sbar ? (
              <SbarPreview sbar={sbar} />
            ) : (
              <Typography fontSize={14} color="text.secondary" mt={0.5}>
                {description}
              </Typography>
            )}

            {!!medias?.length && <MediaList medias={medias} />}
          </CardContent>
        </Card>
      </TimelineContent>
    </TimelineItem>
  )
}

const priorityLabels: Record<EvolutionSbar['priority'], string> = {
  routine: 'Rotina',
  attention: 'Atenção',
  critical: 'Crítico',
}

const clinicalCourseLabels: Record<NonNullable<EvolutionSbar['clinical_course']>, string> = {
  improved: 'Melhorou',
  stable: 'Estável',
  worsened: 'Piorou',
}

const SbarField = ({ label, value }: { label: string; value?: string | null }) => {
  if (!value) return null
  return (
    <Box>
      <Typography fontSize={11} fontWeight={700} color="primary" sx={{ textTransform: 'uppercase' }}>
        {label}
      </Typography>
      <Typography fontSize={14} color="text.secondary" sx={{ whiteSpace: 'pre-wrap' }}>
        {value}
      </Typography>
    </Box>
  )
}

const SbarPreview = ({ sbar }: { sbar: EvolutionSbar }) => (
  <Stack gap={1.25} mt={1.25}>
    <Stack direction="row" gap={1} flexWrap="wrap">
      <Chip label={`Prioridade: ${priorityLabels[sbar.priority]}`} color="primary" size="small" variant="outlined" />
      {sbar.clinical_course && (
        <Chip label={`Evolução: ${clinicalCourseLabels[sbar.clinical_course]}`} size="small" variant="outlined" />
      )}
    </Stack>
    <SbarField label="Situação" value={sbar.situation} />
    <SbarField label="Contexto" value={sbar.background} />
    <SbarField label="Avaliação" value={sbar.assessment} />
    <SbarField label="Plano" value={sbar.recommendation} />
    <SbarField label="Pendências" value={sbar.pending_items} />
    <SbarField label="Alertas" value={sbar.alerts} />
  </Stack>
)

const EvolutionSkeleton = ({ isLatest = false }) => {
  return (
    <TimelineItem>
      <TimelineSeparator>
        <TimelineDot
          color="primary"
          variant={isLatest ? 'filled' : 'outlined'}
          sx={{
            position: 'relative',
            '.MuiTimelineDot-filled&:before': {
              content: "''",
              position: 'absolute',
              border: '2px solid #1976d2',
              padding: '8px',
              borderRadius: '100%',
              transform: 'translate(-50%, -50%)',
            },
          }}
        />
        <TimelineConnector sx={{ bgcolor: 'primary.main' }} />
      </TimelineSeparator>

      <TimelineContent>
        <Card elevation={0} sx={{ borderRadius: 2, p: 2 }}>
          <Box display="flex" justifyContent="space-between" alignItems="start">
            <Box>
              <Skeleton variant="text" width={50} height={16} />
            </Box>
            <Box textAlign="right" sx={{ display: 'flex' }} alignItems="center">
              <Skeleton variant="text" width={40} height={16} sx={{ mr: 1 }} />
              <Skeleton variant="circular" width={24} height={24} />
            </Box>
          </Box>

          <CardContent sx={{ px: 0, pt: 0.5 }}>
            <Skeleton variant="text" width={100} height={20} sx={{ mb: 1 }} />
            <Skeleton variant="text" width="80%" height={16} sx={{ mb: 1 }} />
            <Skeleton variant="text" width="90%" height={16} sx={{ mb: 1 }} />

            <MediaList.Skeleton showCollapseButton={false} />
          </CardContent>
        </Card>
      </TimelineContent>
    </TimelineItem>
  )
}

Evolution.Skeleton = EvolutionSkeleton
