import react from '@vitejs/plugin-react';
import { resolve } from 'path';
import { defineConfig } from 'vite';

export default defineConfig({
  //base: '/',
  plugins: [react()],
  server: {
    port: 5173,
    historyApiFallback: true, // Ensure fallback to index.html in development
  },
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: resolve(__dirname, 'index.html'),
    },
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
});
// https://vitejs.dev/config/