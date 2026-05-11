'use client'

import { Container } from '@mui/material'
import { PropsWithChildren, ReactNode, useRef, useState } from 'react'
import { Footer } from './components/Footer'
import { Main } from '../components/Main'

import { ProfileDrawer } from './components/ProfileDrawer'

type BaseProps = {
  header: ReactNode | null
  speedDial: ReactNode | null
}

export const Base = ({ header, speedDial, children }: PropsWithChildren<BaseProps>) => {
  const [drawer, setDrawer] = useState<{ type: string } | null>(null)
  const openDrawer = (arg: { type: string }) => setDrawer(arg)
  const closeDrawer = () => setDrawer(null)
  const containerRef = useRef<HTMLDivElement>(null)
  return (
    <>
      <Container ref={containerRef} className="grid p-0 h-[100dvh] grid-rows-[auto_1fr_auto] overflow-hidden relative">
        {header}
        <Main>{children}</Main>
        <Footer actionHandler={openDrawer} />
        {speedDial}
      </Container>
      <ProfileDrawer open={drawer?.type === 'profile'} onClose={closeDrawer} containerRef={containerRef} />
    </>
  )
}
