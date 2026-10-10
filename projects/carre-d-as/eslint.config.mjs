import nextConfig from 'eslint-config-next'

// ESLint 9/10 (flat config). `next lint` a été retiré dans Next 16.
export default [
  {
    ignores: ['.next/**', 'node_modules/**', 'lib/generated/**', 'public/**', 'netlify/functions/**/*.js'],
  },
  ...nextConfig,
]
