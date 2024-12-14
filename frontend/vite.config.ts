import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import EnvironmentPlugin from 'vite-plugin-environment';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd());
  return {
    plugins: [
      react(),
      EnvironmentPlugin('all') // Exposes all environment variables
    ],
    define: {
      'process.env.REACT_APP_API_URL': JSON.stringify(env.VITE_API_URL || 'http://localhost:8000'),
    },
    server: {
      host: true,
    },
  };
});
