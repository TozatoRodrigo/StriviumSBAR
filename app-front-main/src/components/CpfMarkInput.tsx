import { InputBaseComponentProps } from '@mui/material'
import React from 'react'
import { IMaskInput } from 'react-imask'

interface CpfMaskProps {
  name: string
  onChange: (event: { target: { name: string; value: string } }) => void
  inputRef: React.Ref<HTMLInputElement>
}

export const CpfMaskInput = React.forwardRef<HTMLInputElement, CpfMaskProps & InputBaseComponentProps>(
  function CpfMaskInput(props, ref) {
    const { onChange, name, ...other } = props

    return (
      <IMaskInput
        {...other}
        mask="000.000.000-00"
        definitions={{ '0': /[0-9]/ }}
        inputRef={ref}
        onAccept={(value: string) => onChange({ target: { name, value } })}
        overwrite
      />
    )
  }
)
