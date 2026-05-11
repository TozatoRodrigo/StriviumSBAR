import { Stack } from '@mui/material'
import { PropsWithChildren } from 'react'

export const Content = ({ children }: PropsWithChildren) => {
  return <Stack flex={1}>{children}</Stack>
}
