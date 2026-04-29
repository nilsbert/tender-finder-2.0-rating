import path from 'path';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: '/ms/rating/',
  plugins: [react()],
  resolve: {
    alias: [
      {
        find: /^@porsche-design-system\/components-react$/,
        replacement: path.resolve(__dirname, 'src/pds-wrapper.tsx')
      }
    ]
  },
  build: {
    outDir: 'dist',
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8999',
        changeOrigin: true,
      },
    },
  },
});