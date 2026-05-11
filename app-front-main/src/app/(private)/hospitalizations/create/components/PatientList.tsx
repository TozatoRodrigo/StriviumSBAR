'use client'

import { Card, FormControl, Radio, RadioGroup, Stack, Typography } from '@mui/material'
import PersonOutlineIcon from '@mui/icons-material/PersonOutline'

import { format } from '@/lib/date'
import { joinFullname } from '@/lib/utils'

type Patient = {
  id: string
  first_name: string
  last_name: string
  birth_date: string
}

type PatientListProps = {
  patients: Patient[]
  selectPatient: { id: string } | null
  onSelect: (id: string) => void
}

export const PatientList = ({ patients, selectPatient, onSelect }: PatientListProps) => {
  if (!patients.length) return null

  return (
    <Stack gap={2}>
      <Typography className="font-normal text-sm text-[#64748B]">Pacientes:</Typography>
      <FormControl>
        <RadioGroup name="patient" onChange={event => onSelect(event.target.value)}>
          <Stack gap={1}>
            {patients.map(({ id, first_name, last_name, birth_date }) => (
              <label className="cursor-pointer" key={id}>
                <Card>
                  <Stack px={2} py={1} direction="row" justifyContent="space-between" alignItems="center" gap={2}>
                    <PersonOutlineIcon sx={{ color: '#64748B' }} />
                    <Stack flex="1" className="font-normal text-sm ">
                      <Typography className="text-[#020617]">{joinFullname(first_name, last_name)}</Typography>
                      <Typography className="text-[#64748B]">{format(birth_date, 'dd/MM/yyyy')}</Typography>
                    </Stack>
                    <Radio value={id} checked={id.toString() === selectPatient?.id} />
                  </Stack>
                </Card>
              </label>
            ))}
          </Stack>
        </RadioGroup>
      </FormControl>
    </Stack>
  )
}
