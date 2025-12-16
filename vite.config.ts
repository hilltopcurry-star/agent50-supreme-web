import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        // 👇 FIX: Yahan maine 5050 kar diya hai taake Python se connect ho
        target: 'http://localhost:5050',
        changeOrigin: true,
      }
    }
  }
})