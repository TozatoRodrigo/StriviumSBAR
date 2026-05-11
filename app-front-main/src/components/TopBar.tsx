import { ChevronLeft } from '@mui/icons-material'
import { Divider, IconButton, IconButtonProps, Stack, Typography } from '@mui/material'
import Link, { LinkProps } from 'next/link'
import { PropsWithChildren } from 'react'

type BackProps = IconButtonProps & LinkProps

const Back = (props: BackProps) => (
  <IconButton {...props} LinkComponent={Link}>
    <ChevronLeft />
  </IconButton>
)
const Title = ({ children }: PropsWithChildren) => <Typography variant="h6">{children}</Typography>

export const TopBar = ({ children }: PropsWithChildren) => {
  return (
    <Stack>
      <div className="flex items-center justify-start px-2 py-0 min-h-[64px] gap-2">{children}</div>
      <Divider />
    </Stack>
  )
}

TopBar.Back = Back
TopBar.Title = Title
