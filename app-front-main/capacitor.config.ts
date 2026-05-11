import type { CapacitorConfig } from '@capacitor/cli'

const config: CapacitorConfig = {
  appId: 'br.com.strivium.link',
  appName: 'Strivium Link',
  webDir: 'out',
  backgroundColor: '#fff',
  server: {
    url: `http://${process.env.LOCAL_IP}:3000`,
    cleartext: true,
  },
}

export default config
