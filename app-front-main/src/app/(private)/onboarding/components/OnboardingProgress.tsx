import Box from '@mui/material/Box'
import LinearProgress from '@mui/material/LinearProgress'
import Typography from '@mui/material/Typography'

import { OnboardingStep, getOnboardingProgress, getOnboardingStepNumber } from './onboardingFlow'

type OnboardingProgressProps = {
  step: OnboardingStep
}

export const OnboardingProgress = ({ step }: OnboardingProgressProps) => {
  return (
    <Box>
      <Typography variant="body2" color="text.secondary">
        Passo {getOnboardingStepNumber(step)} de 5
      </Typography>
      <LinearProgress
        variant="determinate"
        value={getOnboardingProgress(step)}
        sx={{ height: 6, borderRadius: 3, mt: 1 }}
      />
    </Box>
  )
}
