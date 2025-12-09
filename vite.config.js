import { defineConfig } from 'vite';
import { resolve } from 'path';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  root: resolve(__dirname, 'app/static'),
  base: '/static/',
  build: {
    outDir: resolve(__dirname, 'app/static/dist'),
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'app/static/src/main.jsx'),
      },
    },
  },
  server: {
    port: 5173,
    strictPort: false,
    hmr: {
      protocol: 'ws',
      host: 'localhost',
    },
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'app/static/src'),
    },
  },
});
