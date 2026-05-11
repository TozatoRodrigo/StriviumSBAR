'use client'

import { Box, Grid, IconButton } from '@mui/material'
import Image from 'next/image'
import { CloseOutlined } from '@mui/icons-material'

type ImagePreviewProps = {
  image: File | string
  onRemove: () => void
  disabled?: boolean
}

export const ImagePreview = ({ image, onRemove, disabled = false }: ImagePreviewProps) => {
  const preview = typeof image === 'string' ? image : URL.createObjectURL(image)

  return (
    <Grid>
      <Box position="relative">
        <Image src={preview} alt={`preview`} width={100} height={100} style={{ objectFit: 'cover', borderRadius: 8 }} />
        <IconButton
          size="small"
          onClick={onRemove}
          disableRipple
          sx={{
            position: 'absolute',
            top: -8,
            right: -8,
            backgroundColor: 'rgba(0,0,0,.5)',
            boxShadow: 1,
          }}
          disabled={disabled}
        >
          <CloseOutlined
            fontSize="small"
            sx={{
              color: 'white',
            }}
          />
        </IconButton>
      </Box>
    </Grid>
  )
}
