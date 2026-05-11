'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useWorkspace } from '@/contexts/WorkspaceContext'
import { Avatar, Button, Stack, Typography } from '@mui/material'
import SwapHorizIcon from '@mui/icons-material/SwapHoriz'
import Link from 'next/link'

const WorkspaceAvatar = ({ wokspaceName, userName }: { wokspaceName: string; userName: string }) => {
  return (
    <div className="flex gap-4 items-center">
      <Avatar src="/web-app-manifest-192x192.png" style={{ backgroundColor: 'white' }} />
      <Stack>
        <Typography className="font-bold text-[16px]">{wokspaceName}</Typography>
        <Typography variant="caption">{userName}</Typography>
      </Stack>
    </div>
  )
}

export const Header = () => {
  const {
    info: workspaceInfo,
    states: { isRole },
    exit,
  } = useWorkspace()
  const { info: authInfo } = useAuth()

  return (
    <header className="flex justify-between py-2 px-4 bg-[#4283F1] text-white">
      {isRole.admin ? (
        <Link href={`/workspaces/manage?workspace_id=${workspaceInfo?.tenant.id}`}>
          <WorkspaceAvatar wokspaceName={workspaceInfo?.tenant?.name ?? ''} userName={authInfo?.first_name ?? ''} />
        </Link>
      ) : (
        <WorkspaceAvatar wokspaceName={workspaceInfo?.tenant?.name ?? ''} userName={authInfo?.first_name ?? ''} />
      )}
      <Button onClick={exit} endIcon={<SwapHorizIcon />} size="small" sx={{ textTransform: 'none', color: 'inherit' }}>
        Trocar Local
      </Button>
    </header>
  )
}
