'use client'

import { Dialog, DialogContent, Typography } from '@mui/material'

import CloseIcon from '@mui/icons-material/Close'

import { IconButton } from '@mui/material'

import Image from 'next/image'
import { MediaTypeEnum } from '@/types/common'

import type { Media } from '@/hooks/queries/evolutions'

type MediaDialogProps = {
  media: Media | null
  onClose: () => void
}

export const MediaDialog = ({ media, onClose }: MediaDialogProps) => {
  if (!media) return null

  return (
    <Dialog open={!!media} onClose={onClose} fullWidth fullScreen>
      <IconButton
        onClick={onClose}
        sx={{
          position: 'absolute',
          top: 8,
          right: 8,
          zIndex: 1,
        }}
      >
        <CloseIcon />
      </IconButton>

      <DialogContent
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          p: 2,
          minHeight: 300,
        }}
      >
        {media?.type === MediaTypeEnum.IMAGE && (
          <Image
            src={media.file_path}
            alt="media"
            width={600}
            height={600}
            style={{ maxWidth: '100%', height: 'auto', borderRadius: 8 }}
            unoptimized
          />
        )}

        {media?.type === MediaTypeEnum.AUDIO && (
          <>
            <Typography variant="subtitle1" mb={2}>
              Áudio
            </Typography>
            <audio controls style={{ width: '100%' }} autoPlay>
              <source src={media.file_path} />
              Seu navegador não suporta o player de áudio.
            </audio>
          </>
        )}

        {media?.type === MediaTypeEnum.VIDEO && (
          <>
            <Typography variant="subtitle1" mb={2}>
              Vídeo
            </Typography>
            <video
              controls
              autoPlay
              src={media.file_path}
              style={{
                maxWidth: '100%',
                maxHeight: 400,
                borderRadius: 2,
                backgroundColor: 'black',
              }}
            />
          </>
        )}
      </DialogContent>
    </Dialog>
  )
}
