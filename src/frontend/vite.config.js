import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../api/static/react',
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: {
        main: './src/main.jsx'
      },
      output: {
        entryFileNames: 'assets/main-react-app.js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]'
      }
    }
  }
});