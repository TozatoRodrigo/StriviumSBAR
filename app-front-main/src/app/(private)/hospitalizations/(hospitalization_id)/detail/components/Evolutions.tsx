'use client'

import { Skeleton, Typography } from '@mui/material'

import { Box } from '@mui/material'

import { Timeline, timelineItemClasses } from '@mui/lab'

import { Evolution } from './Evolution'
import { EvolutionsHttpResponse } from '@/hooks/queries/evolutions'

type EvolutionsProps = {
  evolutions: EvolutionsHttpResponse[]
}

export const Evolutions = ({ evolutions }: EvolutionsProps) => {
  if (!evolutions.length) {
    return (
      <Typography fontWeight={600} mb={2} flex={1}>
        Ainda não há evoluções registradas para este paciente!
      </Typography>
    )
  }

  return (
    <Box flex={1} sx={{ p: 2, bgcolor: '#F1F5F9' }}>
      <Typography fontWeight={600} mb={2}>
        Histórico de internação
      </Typography>

      <Timeline
        position="right"
        sx={{
          p: 0,
          [`& .${timelineItemClasses.root}:before`]: {
            flex: 0,
            padding: 0,
          },
        }}
      >
        {evolutions.map((evolution, index) => (
          <Evolution key={evolution.id} evolution={evolution} isLatest={index === 0} />
        ))}
      </Timeline>
    </Box>
  )
}

const EvolutionsSkeleton = ({ itemsCount = 3 }) => {
  return (
    <Box sx={{ p: 2, bgcolor: '#F1F5F9' }}>
      <Skeleton variant="text" width={200} height={28} sx={{ mb: 2 }} />

      <Timeline
        position="right"
        sx={{
          p: 0,
          [`& .${timelineItemClasses.root}:before`]: {
            flex: 0,
            padding: 0,
          },
        }}
      >
        {Array.from({ length: itemsCount }).map((_, index) => (
          <Evolution.Skeleton key={index} isLatest={index === 0} />
        ))}
      </Timeline>
    </Box>
  )
}

Evolutions.Skeleton = EvolutionsSkeleton
