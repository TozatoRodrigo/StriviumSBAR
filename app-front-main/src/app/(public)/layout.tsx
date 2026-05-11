'use client'

import { useAuth } from '@/contexts/AuthContext'
import { Container } from '@mui/material'
import { useRouter } from 'next/navigation'
import { PropsWithChildren, useEffect } from 'react'

const Layout = ({ children }: PropsWithChildren) => {
  const {
    states: { isAuth },
  } = useAuth()
  const nav = useRouter()

  useEffect(() => {
    if (isAuth) return nav.push('/')
  }, [isAuth, nav])

  return <Container>{children}</Container>
}

export default Layout
