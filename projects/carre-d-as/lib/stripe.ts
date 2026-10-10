import Stripe from 'stripe'

// Initialize Stripe (will be undefined during build if env var not set)
export const stripe = process.env.STRIPE_SECRET_KEY
  ? new Stripe(process.env.STRIPE_SECRET_KEY, {
      apiVersion: '2026-09-30.endive',
      typescript: true,
    })
  : null

// Helper to ensure stripe is initialized
export function getStripe() {
  if (!stripe) {
    throw new Error('STRIPE_SECRET_KEY is not set')
  }
  return stripe
}

