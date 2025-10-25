import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  // Set base path for GitHub Pages deployment
  base: process.env.NODE_ENV === 'production' ? '/flask-lab-project/' : '/',
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: './vitest.setup.js',
    css: true,
    globals: true,
  },
})
