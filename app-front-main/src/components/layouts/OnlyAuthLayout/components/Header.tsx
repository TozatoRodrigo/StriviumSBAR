'use client'
import { Avatar, Typography } from '@mui/material'

export const Header = () => {
  return (
    <header className="flex justify-center py-2 px-4 bg-[#4283F1] text-white">
      <div className="flex gap-4 items-center">
        <Avatar src="/web-app-manifest-192x192.png" style={{ backgroundColor: 'white' }} />
        <Typography className="font-bold text-[16px]">Strivium Link</Typography>
      </div>
    </header>
  )
}
