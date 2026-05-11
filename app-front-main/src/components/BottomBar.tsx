import { Button, ButtonProps, Divider, Stack } from '@mui/material'
import { PropsWithChildren } from 'react'

const ActionOutlined = (props: ButtonProps) => {
  return (
    <Button
      {...props}
      variant="outlined"
      sx={{
        ...props.sx,
        borderRadius: '999px',
        textTransform: 'none',
      }}
    >
      {props.children}
    </Button>
  )
}

const ActionContained = (props: ButtonProps) => {
  return (
    <Button
      {...props}
      variant="contained"
      sx={{
        ...props.sx,
        borderRadius: '999px',
        textTransform: 'none',
      }}
    >
      {props.children}
    </Button>
  )
}

export const BottomBar = ({ children }: PropsWithChildren) => {
  return (
    <Stack position="sticky" bottom={0} bgcolor="white" zIndex={1}>
      <Divider />
      <Stack className="p-4" direction="row" justifyContent="space-between">
        {children}
      </Stack>
    </Stack>
  )
}

BottomBar.ActionOutlined = ActionOutlined
BottomBar.ActionContained = ActionContained
