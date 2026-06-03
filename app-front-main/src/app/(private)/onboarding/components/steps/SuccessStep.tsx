'use client'

import { Button, Card, CardContent, List, ListItem, ListItemText, Stack, Typography } from '@mui/material'

type SuccessSummary = {
  workspaceName: string
  teamName: string
  inviteCount: number
  patientName: string
  hospitalizationInfo: {
    place: string
    sector: string
  }
}

type SuccessStepProps = {
  summary: SuccessSummary
  onComplete: () => void
}

export const SuccessStep = ({ summary, onComplete }: SuccessStepProps) => {
  return (
    <Stack className="p-4" gap={3}>
      <Stack gap={1} textAlign="center">
        <Typography variant="h5">Tudo pronto</Typography>
        <Typography color="text.secondary">
          Seu local de trabalho foi configurado e o paciente já está aguardando atendimento.
        </Typography>
      </Stack>

      <Card>
        <CardContent>
          <List dense>
            <ListItem>
              <ListItemText primary="Local de trabalho" secondary={summary.workspaceName} />
            </ListItem>
            <ListItem>
              <ListItemText primary="Equipe" secondary={summary.teamName} />
            </ListItem>
            <ListItem>
              <ListItemText primary="Paciente" secondary={summary.patientName} />
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Internação"
                secondary={`${summary.hospitalizationInfo.place} - ${summary.hospitalizationInfo.sector}`}
              />
            </ListItem>
            <ListItem>
              <ListItemText primary="Convites enviados" secondary={String(summary.inviteCount)} />
            </ListItem>
          </List>
        </CardContent>
      </Card>

      <Button variant="contained" fullWidth onClick={onComplete}>
        Ir para pendências
      </Button>
    </Stack>
  )
}
