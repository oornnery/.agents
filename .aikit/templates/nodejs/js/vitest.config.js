import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    dir: 'tests',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      include: ['src/**/*.js'],
    },
  },
});
