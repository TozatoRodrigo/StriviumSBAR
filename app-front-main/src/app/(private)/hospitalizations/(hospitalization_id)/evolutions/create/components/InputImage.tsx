'use client'
import { Button } from '@mui/material'

import AddIcon from '@mui/icons-material/Add'
import { useRef } from 'react'

type InputImageProps = {
  onAddImage: (files: File[]) => void
  disabled?: boolean
}

export const InputImage = ({ onAddImage, disabled = false }: InputImageProps) => {
  const inputImagesRef = useRef<HTMLInputElement>(null)
  const handleClick = () => {
    inputImagesRef.current?.click()
  }

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (files) {
      onAddImage(Array.from(files))
    }
  }
  return (
    <>
      <Button
        onClick={handleClick}
        variant="outlined"
        startIcon={<AddIcon />}
        sx={{ borderRadius: '999px' }}
        disabled={disabled}
      >
        Adicionar imagem
      </Button>
      <input
        type="file"
        ref={inputImagesRef}
        style={{ display: 'none' }}
        accept="image/*"
        multiple
        onChange={handleFileChange}
      />
    </>
  )
}
