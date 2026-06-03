const optimizePackageImports =
  process.env.NEXT_ENABLE_OPTIMIZE_PACKAGE_IMPORTS === 'true'
    ? {
        optimizePackageImports: [
          '@mui/material',
          '@mui/icons-material',
          '@mui/lab',
          '@mui/x-date-pickers',
          '@tanstack/react-query',
        ],
      }
    : undefined

const nextConfig = {
  reactStrictMode: true,
  images: {
    unoptimized: true,
  },
  turbopack: {
    resolveAlias: {
      axios: 'axios/dist/browser/axios.cjs',
    },
  },
  webpack: config => {
    config.resolve.alias = {
      ...config.resolve.alias,
      axios: 'axios/dist/browser/axios.cjs',
    }

    return config
  },
  ...(optimizePackageImports ? { experimental: optimizePackageImports } : {}),
  ...(process.env.NODE_ENV === 'production' ? { output: 'export' } : {}),
}

export default nextConfig
