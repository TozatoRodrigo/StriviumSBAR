'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useWorkspace } from '@/contexts/WorkspaceContext'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

const mainPage = '/hospitalizations/pendings'

export default function App() {
  const router = useRouter()
  const {
    states: { isAuth },
  } = useAuth()
  const {
    states: { isAuth: isAuthOnWorkspace },
  } = useWorkspace()

  useEffect(() => {
    if (!isAuth) return router.push('/signin')
    if (!isAuthOnWorkspace) return router.push('/workspaces')
    router.push(mainPage)
  }, [isAuth, isAuthOnWorkspace, router])

  return null
}
