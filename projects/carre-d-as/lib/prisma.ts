import { createPrismaClient } from './db-client'
import type { PrismaClient } from './generated/prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

// Retry logic for database operations
async function withRetry<T>(
  operation: () => Promise<T>,
  maxRetries: number = 3,
  delay: number = 1000
): Promise<T> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await operation()
    } catch (error: any) {
      console.log(`Database operation attempt ${attempt} failed:`, error.message)
      
      if (attempt === maxRetries) {
        throw error
      }
      
      // Wait before retrying
      await new Promise(resolve => setTimeout(resolve, delay * attempt))
    }
  }
  throw new Error('Max retries exceeded')
}

// Connection pool configuration to prevent connection exhaustion
const createClient = () => {
  return createPrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
    // Connection pooling is handled by Supabase's transaction pooler
    // with pgbouncer=true in the DATABASE_URL (adaptateur pg, Prisma 7)
  })
}

export const prisma: PrismaClient = globalForPrisma.prisma ?? createClient()

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma

// Export retry wrapper for use in server actions
export { withRetry }

// Graceful shutdown handling
if (process.env.NODE_ENV !== 'production') {
  process.on('beforeExit', async () => {
    await prisma.$disconnect()
  })
}

export default prisma


