import { Stack, Typography } from '@mui/material'
import Image from 'next/image'

export const WorkspacesInvitesEmptyList = () => {
  return (
    <Stack className="p-4" flex={1} gap={2}>
      <Image
        className="self-center"
        src="/empty_workspaces.png"
        alt="Sem locais de trabalho"
        unoptimized
        width={200}
        height={200}
      />
      <Stack alignItems="center">
        <Typography className="font-normal text-[#020617] text-xl">
          Você ainda não possui convites para nenhum local de trabalho!
        </Typography>
      </Stack>
    </Stack>
  )
}
