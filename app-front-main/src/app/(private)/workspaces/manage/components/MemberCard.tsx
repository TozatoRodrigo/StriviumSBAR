import { Box, Typography, Card, CardContent, IconButton, Skeleton } from '@mui/material'
import { MoreVert } from '@mui/icons-material'
import { rolesOptions } from '@/constants/roles'
import { joinFullname } from '@/lib/utils'

type MemberCardProps = {
  id: string
  tenant_id: string
  user_id: string
  user: {
    id: string
    first_name: string
    last_name: string
    email: string
  }
  role_id: string
  role: {
    id: string
    name: string
    description: string
  }
  created_at: string
  updated_at: string
}

export const MemberCard = ({ user, role }: MemberCardProps) => {
  return (
    <>
      <Card variant="outlined">
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="start">
            <Box>
              <Typography variant="subtitle1">{joinFullname(user.first_name, user.last_name)}</Typography>
              <Typography variant="body2" color="text.secondary">
                {user.email}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {rolesOptions.find(_role => _role.id === role.name)?.label ?? ''}
              </Typography>
              {/* TODO: implementar na api */}
              <Typography variant="caption" color={1 ? 'success.main' : 'error.main'}>
                {1 ? 'Ativo' : 'Inativo'}
              </Typography>
            </Box>
          </Box>
        </CardContent>
      </Card>
    </>
  )
}

const MemberCardSkeleton = () => {
  return (
    <Card variant="outlined">
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="start">
          <Box>
            <Typography variant="subtitle1">
              <Skeleton width={120} />
            </Typography>
            <Typography variant="body2" color="text.secondary">
              <Skeleton width={180} />
            </Typography>
            <Typography variant="body2" color="text.secondary">
              <Skeleton width={100} />
            </Typography>
            <Typography variant="caption" color="text.secondary">
              <Skeleton width={60} />
            </Typography>
          </Box>
          <IconButton disabled>
            <MoreVert />
          </IconButton>
        </Box>
      </CardContent>
    </Card>
  )
}

MemberCard.Skeleton = MemberCardSkeleton
