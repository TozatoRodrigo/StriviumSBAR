'use client'

import { useEffect, useRef, useState } from 'react'
import { useRouter } from 'next/navigation'

import { ErrorState } from '@/components/ErrorState'
import { Loader } from '@/components/Loader'
import { useWorkspace } from '@/contexts/WorkspaceContext'
import { useWorkspaces } from '@/hooks/queries/workspaces'
import { useWorkspacesPendingInvites } from '@/hooks/queries/workspacesUser'
import { OnboardingWizard } from './components/OnboardingWizard'
import { shouldEnterOnboarding } from './components/onboardingFlow'

export default function OnboardingPage() {
  const router = useRouter()
  const {
    states: { isAuth: isAuthOnWorkspace },
  } = useWorkspace()
  const wasAuthOnWorkspaceAtEntry = useRef(isAuthOnWorkspace)

  const workspacesQuery = useWorkspaces()
  const invitesQuery = useWorkspacesPendingInvites()

  const [preflightState, setPreflightState] = useState<
    'loading' | 'allow' | 'error' | 'redirect-workspaces' | 'redirect-pendings'
  >(wasAuthOnWorkspaceAtEntry.current ? 'redirect-pendings' : 'loading')

  useEffect(() => {
    if (preflightState !== 'loading') return

    if (workspacesQuery.isLoading || invitesQuery.isLoading) return

    if (workspacesQuery.isError || invitesQuery.isError) {
      setPreflightState('error')
      return
    }

    const workspaceCount = workspacesQuery.data?.data.length ?? 0
    const pendingInvitesCount = invitesQuery.data?.data.length ?? 0
    const canEnterOnboarding = shouldEnterOnboarding({ workspaceCount, pendingInvitesCount })

    if (!canEnterOnboarding) {
      setPreflightState('redirect-workspaces')
      return
    }

    setPreflightState('allow')
  }, [
    invitesQuery.data?.data.length,
    invitesQuery.isError,
    invitesQuery.isLoading,
    preflightState,
    workspacesQuery.data?.data.length,
    workspacesQuery.isError,
    workspacesQuery.isLoading,
  ])

  useEffect(() => {
    if (preflightState === 'redirect-pendings') {
      router.replace('/hospitalizations/pendings')
      return
    }

    if (preflightState === 'redirect-workspaces') {
      router.replace('/workspaces')
    }
  }, [preflightState, router])

  if (preflightState === 'loading' || preflightState === 'redirect-pendings' || preflightState === 'redirect-workspaces') {
    return <Loader />
  }

  if (preflightState === 'error') {
    return (
      <ErrorState
        onRetry={() => {
          setPreflightState('loading')
          void Promise.all([workspacesQuery.refetch(), invitesQuery.refetch()])
        }}
      />
    )
  }

  return <OnboardingWizard />
}
