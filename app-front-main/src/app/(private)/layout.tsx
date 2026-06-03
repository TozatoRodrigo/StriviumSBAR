'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useWorkspace } from '@/contexts/WorkspaceContext'
import { usePathname, useRouter } from 'next/navigation'
import { PropsWithChildren, useEffect } from 'react'

const onlyAuthRoutes = ['/workspaces', '/workspaces/create', '/onboarding']

export default function Private({ children }: PropsWithChildren) {
  const {
    states: { isAuth },
  } = useAuth()

  const {
    states: { isAuth: isAuthOnWorkspace },
  } = useWorkspace()
  const router = useRouter()

  const pathname = usePathname()

  useEffect(() => {
    if (!isAuth) return router.push('/signin')
    if (!isAuthOnWorkspace && !onlyAuthRoutes.includes(pathname)) {
      return router.push('/workspaces')
    }
  }, [isAuth, isAuthOnWorkspace, pathname, router])

  return <>{children}</>
}
