import { PrismaPg } from '@prisma/adapter-pg'
import { PrismaClient } from './generated/prisma/client'

/**
 * Fabrique unique du client Prisma (Prisma 7 : le client exige un adaptateur de driver).
 * Utilisée par l'app (lib/prisma.ts), les fonctions Netlify, le seed et les scripts.
 *
 * DATABASE_URL pointe vers le pooler Supabase (transaction mode, pgbouncer=true).
 */
export function createPrismaClient(
  options: { log?: ('query' | 'info' | 'warn' | 'error')[] } = {}
): PrismaClient {
  // Le pool pg est paresseux : aucune connexion avant la première requête.
  // Pas d'erreur à la construction (le build Next peut évaluer ce module sans base).
  const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL ?? '' })

  return new PrismaClient({
    adapter,
    log: options.log,
  })
}
