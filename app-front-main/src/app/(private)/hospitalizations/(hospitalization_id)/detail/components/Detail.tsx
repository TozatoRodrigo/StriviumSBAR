'use client'

import { BottomBar } from '@/components/BottomBar'
import { useHospitalization } from '@/hooks/queries/hospitalizations'
import { DetailHeader } from './DetailHeader'
import { Evolutions } from './Evolutions'
import { Box, Skeleton } from '@mui/material'
import Link from 'next/link'
import { useEvolutions } from '@/hooks/queries/evolutions'
import { useMemo } from 'react'
import { Content } from '@/components/Content'
import { ErrorState } from '@/components/ErrorState'
import { EmptyState } from '@/components/EmptyState'
import { useFromQuery } from '@/hooks/queryParams/from'

const EvolutionsWrapper = ({ hospitalization_id }: { hospitalization_id: string }) => {
  const { data, isError, isLoading, refetch } = useEvolutions(hospitalization_id)

  const evolutions = useMemo(() => data?.data, [data?.data])

  if (isLoading) return <Evolutions.Skeleton />
  if (isError || !evolutions) return <ErrorState onRetry={refetch} />
  if (!evolutions.length) return <EmptyState />

  return <Evolutions evolutions={evolutions} />
}

export const Detail = ({ hospitalization_id }: { hospitalization_id: string }) => {
  const { data, isError, isLoading, refetch } = useHospitalization(hospitalization_id)
  const { backHref, fromQuery } = useFromQuery()
  const createEvolutionHref = `/hospitalizations/evolutions/create/?hospitalization_id=${hospitalization_id}${
    fromQuery ? `&${fromQuery}` : ''
  }`

  if (isLoading) return <DetailHeader.Skeleton />
  if (isError || !data) return <ErrorState onRetry={refetch} />

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
      <DetailHeader hospitalization={data} />

      <Content>
        <EvolutionsWrapper hospitalization_id={hospitalization_id} />
      </Content>

      <BottomBar>
        <BottomBar.ActionOutlined component={Link} href={backHref}>
          Voltar
        </BottomBar.ActionOutlined>
        <BottomBar.ActionContained component={Link} href={createEvolutionHref} disabled={data.status !== 'active'}>
          Registrar visita
        </BottomBar.ActionContained>
      </BottomBar>
    </Box>
  )
}

const DetailSkeleton = () => {
  return (
    <div>
      <DetailHeader.Skeleton />
      <Evolutions.Skeleton />
      <BottomBar>
        <BottomBar.ActionOutlined disabled>
          <Skeleton variant="text" width={60} height={24} />
        </BottomBar.ActionOutlined>
        <BottomBar.ActionContained disabled>
          <Skeleton variant="text" />
        </BottomBar.ActionContained>
      </BottomBar>
    </div>
  )
}

Detail.Skeleton = DetailSkeleton
