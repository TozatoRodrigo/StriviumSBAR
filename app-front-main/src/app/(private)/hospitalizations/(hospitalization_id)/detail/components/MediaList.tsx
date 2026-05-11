'use client'

import { Button, Collapse, Skeleton, Stack } from '@mui/material'
import { useState } from 'react'

import { IconButton, Avatar } from '@mui/material'

import Image from 'next/image'
import { PlayCircle, SmartDisplay } from '@mui/icons-material'
import { useResizeObserver } from '@/hooks/useResizeObserver'
import { MediaTypeEnum } from '@/types/common'
import { parseEnumType } from '@/lib/utils'
import { MediaDialog } from './MediaDialog'

import type { Media } from '@/hooks/queries/evolutions'

type MediaListProps = {
  medias: Media[]
  collapseHeight?: number
  transitionDuration?: number
}

export const MediaList = ({ medias, collapseHeight = 64, transitionDuration = 300 }: MediaListProps) => {
  const [expanded, setExpanded] = useState(false)
  const { ref, height } = useResizeObserver<HTMLDivElement>()
  const shouldCollapse = height > collapseHeight
  const [selected, setSelected] = useState<Media | null>(null)

  return (
    <>
      <Stack>
        <Collapse
          in={expanded || !shouldCollapse}
          collapsedSize={collapseHeight}
          timeout={transitionDuration}
          sx={{ overflow: 'hidden' }}
        >
          <Stack
            ref={ref}
            direction="row"
            gap={1}
            mt={1}
            flexWrap="wrap"
            sx={{
              px: 0.5,
              py: 0.5,
            }}
          >
            {medias.map(media =>
              parseEnumType(media.type, MediaTypeEnum) ? (
                <IconButton key={media.id} onClick={() => setSelected(media)}>
                  <Avatar
                    variant="rounded"
                    sx={{
                      bgcolor: '#f2f2f5',
                      width: 40,
                      height: 40,
                    }}
                  >
                    {media.type === MediaTypeEnum.IMAGE && (
                      <Image
                        src={media.file_path}
                        alt={media.file_name}
                        unoptimized
                        width={40}
                        height={40}
                        style={{ objectFit: 'cover', borderRadius: 4 }}
                      />
                    )}
                    {media.type === MediaTypeEnum.AUDIO && <PlayCircle color="warning" />}
                    {media.type === MediaTypeEnum.VIDEO && <SmartDisplay color="error" />}
                  </Avatar>
                </IconButton>
              ) : null
            )}
          </Stack>
        </Collapse>

        {shouldCollapse && (
          <Button size="small" onClick={() => setExpanded(prev => !prev)} sx={{ mt: 1 }}>
            {expanded ? 'Ver menos' : 'Ver mais'}
          </Button>
        )}
      </Stack>
      <MediaDialog media={selected} onClose={() => setSelected(null)} />
    </>
  )
}

const MediaListSkeleton = ({
  itemsCount = 6,
  collapseHeight = 64,
  transitionDuration = 300,
  expanded = false,
  showCollapseButton = true,
}) => {
  return (
    <Stack>
      <Collapse
        in={expanded || !showCollapseButton}
        collapsedSize={collapseHeight}
        timeout={transitionDuration}
        sx={{ overflow: 'hidden' }}
      >
        <Stack
          direction="row"
          gap={1}
          mt={1}
          flexWrap="wrap"
          sx={{
            px: 0.5,
            py: 0.5,
          }}
        >
          {Array.from({ length: itemsCount }).map((_, index) => (
            <IconButton key={index}>
              <Avatar
                variant="rounded"
                sx={{
                  bgcolor: '#f2f2f5',
                  width: 40,
                  height: 40,
                }}
              >
                <Skeleton variant="rectangular" width={40} height={40} sx={{ borderRadius: 1 }} />
              </Avatar>
            </IconButton>
          ))}
        </Stack>
      </Collapse>

      {showCollapseButton && <Skeleton variant="rectangular" width={80} height={24} sx={{ mt: 1, borderRadius: 1 }} />}
    </Stack>
  )
}

MediaList.Skeleton = MediaListSkeleton
