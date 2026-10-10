import 'dotenv/config'
import { defineConfig } from 'prisma/config'

// Prisma 7 : l'URL est lue ici (CLI uniquement : migrate, db push, studio).
// DIRECT_URL (connexion directe, hors pooler) est préférée pour les migrations.
export default defineConfig({
  schema: 'prisma/schema.prisma',
  datasource: {
    url: process.env.DIRECT_URL || process.env.DATABASE_URL || '',
  },
})
