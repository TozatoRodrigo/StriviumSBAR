import { InputBaseComponentProps } from '@mui/material'
import React from 'react'
import { IMaskInput } from 'react-imask'

export const PhoneMaskInput = React.forwardRef<HTMLInputElement, InputBaseComponentProps>(function PhoneMaskInput(
  props,
  ref
) {
  const { onChange, name, ...other } = props

  return (
    <IMaskInput
      {...other}
      mask="(00) 00000-0000"
      definitions={{ '0': /[0-9]/ }}
      inputRef={ref}
      onAccept={(value: string) => onChange({ target: { name, value } })}
      overwrite
    />
  )
})
