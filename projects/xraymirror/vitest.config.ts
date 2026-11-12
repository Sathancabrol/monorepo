import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'node',
    include: ['src/**/*.test.ts', 'tests/**/*.test.tsx'],
    environmentOptions: {
      jsdom: { pretendToBeVisual: true },
    },
    setupFiles: ['tests/setup.ts'],
  },
});
