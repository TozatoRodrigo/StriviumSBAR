import { FilledInput, FilledInputProps } from '@mui/material'
import InputAdornment from '@mui/material/InputAdornment'
import IconButton from '@mui/material/IconButton'
import Visibility from '@mui/icons-material/Visibility'
import VisibilityOff from '@mui/icons-material/VisibilityOff'
import { useState } from 'react'

export const InputPassword = (props: FilledInputProps) => {
  const [showPassword, setShowPassword] = useState(false)

  const handleClickShowPassword = () => setShowPassword(show => !show)

  const handleMouseDownPassword = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault()
  }

  const handleMouseUpPassword = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault()
  }

  return (
    <FilledInput
      placeholder="Senha"
      autoComplete="current-password"
      {...props}
      type={showPassword ? 'text' : 'password'}
      slotProps={{
        input: {
          sx: {
            '&.MuiFilledInput-input': {
              padding: '1rem',
            },
          },
        },
      }}
      endAdornment={
        <InputAdornment position="end">
          <IconButton
            aria-label={showPassword ? 'hide the password' : 'display the password'}
            onClick={handleClickShowPassword}
            onMouseDown={handleMouseDownPassword}
            onMouseUp={handleMouseUpPassword}
          >
            {showPassword ? <VisibilityOff /> : <Visibility />}
          </IconButton>
        </InputAdornment>
      }
    />
  )
}
