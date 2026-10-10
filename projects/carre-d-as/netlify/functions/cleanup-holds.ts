import { schedule } from '@netlify/functions'
import { createPrismaClient } from '../../lib/db-client'

const prisma = createPrismaClient()

const cleanupHolds = async () => {
  try {
    const now = new Date()

    // Delete expired slot holds
    const result = await prisma.slotHold.deleteMany({
      where: {
        expiresAt: {
          lte: now,
        },
      },
    })

    console.log(`Cleaned up ${result.count} expired slot holds`)

    return {
      statusCode: 200,
      body: JSON.stringify({
        message: `Cleaned up ${result.count} expired holds`,
      }),
    }
  } catch (error) {
    console.error('Error cleaning up holds:', error)
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to cleanup holds' }),
    }
  } finally {
    await prisma.$disconnect()
  }
}

// Run every minute
export const handler = schedule('* * * * *', cleanupHolds)


