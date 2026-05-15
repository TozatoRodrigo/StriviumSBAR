'use client'

import { EmptyState } from '@/components/EmptyState'
import { ErrorState } from '@/components/ErrorState'
import { HospitalizationInfo, Hospitalizations } from '@/components/Hospitalizations'
import { InfiniteLoading } from '@/components/InfiniteLoading'
import { usePendings } from '@/hooks/queries/hospitalizations'
import { useDebounce } from '@/hooks/useDebounce'
import SearchIcon from '@mui/icons-material/Search'
import { IconButton, InputAdornment, Stack, TextField } from '@mui/material'
import CloseIcon from '@mui/icons-material/Close'
import { useMemo, useState } from 'react'
import { filterHospitalizationsBySearch } from '../utils/localSearch'

export default function Pendings() {
  const [search, setSearch] = useState('')
  const searchDebounced = useDebounce(search, 300)
  const { data, fetchNextPage, hasNextPage, isLoading, isFetchingNextPage, isError, refetch } = usePendings(5)

  const hospitalizations = useMemo<HospitalizationInfo[]>(
    () => data?.pages.flatMap(page => page.data) ?? [],
    [data?.pages]
  )
  const filteredHospitalizations = useMemo(
    () => filterHospitalizationsBySearch(hospitalizations, searchDebounced),
    [hospitalizations, searchDebounced]
  )

  if (isLoading) return <Hospitalizations.Skeleton />
  if (isError || !hospitalizations) return <ErrorState onRetry={refetch} />

  return (
    <Stack gap={2}>
      <TextField
        value={search}
        onChange={event => setSearch(event.target.value)}
        placeholder="Buscar por paciente, setor, motivo ou local"
        aria-label="Buscar internações pendentes"
        slotProps={{
          input: {
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
            endAdornment: search ? (
              <InputAdornment position="end">
                <IconButton
                  aria-label="Limpar busca de internações pendentes"
                  title="Limpar busca"
                  onClick={() => setSearch('')}
                  edge="end"
                  size="small"
                >
                  <CloseIcon fontSize="small" />
                </IconButton>
              </InputAdornment>
            ) : undefined,
            sx: { borderRadius: '999px' },
          },
        }}
      />
      <div className="grid gap-2">
        {searchDebounced && !filteredHospitalizations.length ? (
          <EmptyState
            title="Nenhum resultado para a busca"
            message={`Não encontramos internações pendentes para "${searchDebounced}".`}
          />
        ) : (
          <Hospitalizations hospitalizations={filteredHospitalizations} />
        )}
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
