'use client'

import { Box, Button, InputAdornment, Stack, TextField, Typography } from '@mui/material'
import SearchIcon from '@mui/icons-material/Search'
import AddIcon from '@mui/icons-material/Add'
import Link from 'next/link'
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import { withCallbackRoute, withFormStepsParams } from '@/lib/utils'
import { usePatientParams } from '@/hooks/queryParams/patients'
import { usePatients } from '@/hooks/queries/patients'
import { useDebounce } from '@/hooks/useDebounce'
import { PatientList } from './PatientList'

type PatientStepProps = {
  selectedId: string
  onSelect: (id: string) => void
}

export function PatientStep({ selectedId, onSelect }: PatientStepProps) {
  const { patient_id, removeParam } = usePatientParams()
  const [search, setSearch] = useState('')
  const searchDebounced = useDebounce(search, 500)
  const previousSearch = useRef(search)

  const { data: patientsData, isLoading: isLoadingPatients } = usePatients({
    params: { search: searchDebounced },
    options: { enabled: !!searchDebounced, keyword: 'hospitalization-page' },
  })
  const patients = useMemo(() => patientsData?.data, [patientsData?.data])

  const {
    data: patientsByIdData,
    isLoading: isLoadingPatientsById,
    isError: isErrorPatientsById,
  } = usePatients({
    params: { search: patient_id ?? '' },
    options: { enabled: !!patient_id, keyword: 'hospitalization-page-search-patient-id' },
  })

  const patientsById = useMemo(() => patientsByIdData?.data, [patientsByIdData?.data])

  const isLoading = useMemo(
    () => isLoadingPatients || isLoadingPatientsById,
    [isLoadingPatients, isLoadingPatientsById]
  )

  const patientsToDisplay = useMemo(() => {
    if (patient_id && patientsById?.length && !search) {
      return patientsById
    } else {
      return patients
    }
  }, [patient_id, patients, patientsById, search])

  const autoSelectPatient = useCallback(() => {
    if (patient_id && !!patientsById?.length) {
      onSelect(patient_id)
    }
  }, [onSelect, patient_id, patientsById?.length])

  const resetPatientIdParamOnSearch = useCallback(() => {
    if (patient_id && !!search) {
      removeParam('patient_id')
    }
  }, [patient_id, removeParam, search])

  const resetPatientIdParamOnFetchError = useCallback(() => {
    if (patient_id && !!isErrorPatientsById) {
      removeParam('patient_id')
    }
  }, [isErrorPatientsById, patient_id, removeParam])

  const resetSelectedIdOnSearch = useCallback(() => {
    if (search !== previousSearch.current) {
      onSelect('')
      previousSearch.current = search
    }
  }, [onSelect, search])

  useEffect(autoSelectPatient)
  useEffect(resetPatientIdParamOnSearch)
  useEffect(resetPatientIdParamOnFetchError)
  useEffect(resetSelectedIdOnSearch)

  return (
    <Stack gap={2}>
      <Stack direction="row" alignItems="center" spacing={1}>
        <Box
          sx={{
            width: 28,
            height: 28,
            bgcolor: '#4283F1',
            borderRadius: '50%',
            color: 'white',
            fontSize: 14,
            fontWeight: 'bold',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          1
        </Box>
        <Box>
          <Typography variant="caption" fontWeight="medium" color="text.secondary">
            Passo 1 de 2
          </Typography>
          <Typography variant="body1" fontWeight="normal">
            Paciente
          </Typography>
        </Box>
      </Stack>

      <TextField
        autoFocus
        value={search}
        onChange={event => setSearch(event.target.value)}
        slotProps={{
          input: {
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
            sx: {
              borderRadius: '999px',
            },
          },
        }}
        placeholder="Buscar por paciente"
      />

      <Button
        LinkComponent={Link}
        href={withFormStepsParams(withCallbackRoute('/patients/create', '/hospitalizations/create'), '1', '2')}
        variant="outlined"
        startIcon={<AddIcon />}
        sx={{ borderRadius: '999px' }}
      >
        Adicionar paciente
      </Button>

      {!!patientsToDisplay?.length && !isLoading && (
        <PatientList patients={patientsToDisplay} selectPatient={{ id: selectedId }} onSelect={onSelect} />
      )}
    </Stack>
  )
}
