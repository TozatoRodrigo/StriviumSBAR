import { useSearchParams } from 'next/navigation'

export const useCallbackParams = () => {
  const searchParams = useSearchParams()
  const callbackUrl = searchParams.get('callback')

  return { callbackUrl }
}

export const useFormStepsParams = () => {
  const searchParams = useSearchParams()
  const current_step = searchParams.get('current_step')
  const steps = searchParams.get('steps')

  const withFormSteps = !!current_step && !!steps

  return { current_step, steps, withFormSteps }
}

export const useRemoveParams = () => (params: string | string[]) => {
  const url = new URL(window.location.href)

  if (Array.isArray(params)) {
    params.forEach(param => {
      url.searchParams.delete(param)
    })
  } else {
    url.searchParams.delete(params)
  }

  window.history.replaceState(null, '', url.toString())
}

export const useSetParam = () => (param: string, value: string) => {
  const url = new URL(window.location.href)

  url.searchParams.set(param, value)

  window.history.replaceState(null, '', url.toString())
}
