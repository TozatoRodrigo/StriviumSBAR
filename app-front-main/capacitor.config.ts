import type { CapacitorConfig } from '@capacitor/cli'

const remoteServerUrl = process.env.CAPACITOR_SERVER_URL?.trim()

const remoteServerConfig: Pick<CapacitorConfig, 'server'> = remoteServerUrl
  ? {
      server: {
        url: remoteServerUrl,
        cleartext: remoteServerUrl.startsWith('http://'),
      },
    }
  : {}

const liveReloadServer: Pick<CapacitorConfig, 'server'> =
  !remoteServerUrl && process.env.CAPACITOR_LIVE_RELOAD === 'true' && process.env.LOCAL_IP
    ? {
        server: {
          url: `http://${process.env.LOCAL_IP}:3000`,
          cleartext: true,
        },
      }
    : {}

const config: CapacitorConfig = {
  appId: 'br.com.strivium.link',
  appName: 'Strivium Link',
  webDir: 'out',
  backgroundColor: '#ffffff',
  ...remoteServerConfig,
  ...liveReloadServer,
}

export default config
