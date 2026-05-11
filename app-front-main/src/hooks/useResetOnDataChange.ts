import { useCallback, useEffect, useRef } from 'react'

export function useResetOnDataChange<T extends object>(data: T, onChange: (newData: T) => void) {
  const previousDataRef = useRef<T>(data)

  const refresh = useCallback(() => {
    const prev = previousDataRef.current
    let hasDiff = false

    for (const key in data) {
      if (data[key] !== prev[key]) {
        hasDiff = true
        break
      }
    }

    if (hasDiff) {
      previousDataRef.current = data
      onChange(data)
    }
  }, [data, onChange])

  useEffect(refresh, [refresh])
}
