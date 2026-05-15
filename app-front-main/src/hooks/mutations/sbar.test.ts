import { describe, expect, it } from 'vitest'

import { resolveSbarExtractEndpoint } from './sbar'

describe('resolveSbarExtractEndpoint', () => {
  it('avoids duplicated /api prefix when base url already ends with /api', () => {
    expect(resolveSbarExtractEndpoint('https://strivium.link.servidortozato.cloud/api')).toBe('/sbar/extract')
    expect(resolveSbarExtractEndpoint('https://strivium.link.servidortozato.cloud/api/')).toBe('/sbar/extract')
  })

  it('keeps legacy endpoint for direct api base urls', () => {
    expect(resolveSbarExtractEndpoint('http://localhost:55000')).toBe('/api/sbar/extract')
    expect(resolveSbarExtractEndpoint(undefined)).toBe('/api/sbar/extract')
  })
})
