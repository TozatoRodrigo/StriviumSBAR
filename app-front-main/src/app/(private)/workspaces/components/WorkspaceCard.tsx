import { Card, Skeleton, Stack, Typography } from '@mui/material'
import BusinessCenterOutlinedIcon from '@mui/icons-material/BusinessCenterOutlined'
import { useWorkspace } from '@/contexts/WorkspaceContext'

type WorkspaceCardProps = { id: string; name: string }

export const WorkspaceCard = ({ id, name }: WorkspaceCardProps) => {
  const {
    select,
    states: { isAuthenticating },
  } = useWorkspace()

  const handleClick = () => {
    if (!isAuthenticating) select(id)
  }

  const className = `transition-all ${
    isAuthenticating ? 'opacity-50 pointer-events-none cursor-not-allowed' : 'cursor-pointer'
  }`

  return (
    <Card onClick={handleClick} className={className}>
      <Stack p={2} direction="row" justifyContent="space-between" alignItems="center" gap={2}>
        <BusinessCenterOutlinedIcon sx={{ color: '#64748B' }} />
        <Stack flex="1" className="font-normal text-sm ">
          <Typography className="text-[#020617]">{name}</Typography>
        </Stack>
      </Stack>
    </Card>
  )
}

const WorkspaceCardSkeleton = () => {
  return (
    <Card>
      <Stack p={2} direction="row" justifyContent="space-between" alignItems="center" gap={2}>
        <Skeleton variant="circular">
          <BusinessCenterOutlinedIcon />
        </Skeleton>
        <Stack flex="1">
          <Typography className="text-sm font-normal text-[#020617]">
            <Skeleton width="80%" />
          </Typography>
        </Stack>
      </Stack>
    </Card>
  )
}

WorkspaceCard.Skeleton = WorkspaceCardSkeleton
