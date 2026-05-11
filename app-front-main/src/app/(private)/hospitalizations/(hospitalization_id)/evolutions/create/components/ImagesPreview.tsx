import { Box, Grid, Typography } from '@mui/material'
import { ImagePreview } from './ImagePreview'
import { Media } from '@/hooks/queries/evolutions'

type ImagesPreviewProps = {
  images: (File | Media)[]
  onRemove: (item: number | Media) => void
  disabled?: boolean
}

const isFile = (item: File | Media): item is File => (item as File).name !== undefined

export const ImagesPreview = ({ images, onRemove, disabled = false }: ImagesPreviewProps) => {
  return (
    <Box>
      <Typography variant="subtitle2" color="text.secondary" mb={1}>
        Imagens Anexadas:
      </Typography>

      <Grid container spacing={2} mt={2}>
        {images.map((item, index) => (
          <ImagePreview
            key={index}
            image={isFile(item) ? item : item.file_path}
            onRemove={() => onRemove(isFile(item) ? index : item)}
            disabled={disabled}
          />
        ))}
      </Grid>
    </Box>
  )
}
