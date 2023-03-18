import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import AutoImport from 'unplugin-auto-import/vite';
import Components from 'unplugin-vue-components/vite';
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers';
import viteSentry from 'vite-plugin-sentry';
import { config } from "./config";

const sentryConfig = {
  configFile: './.sentryclirc',
  release: config.version,
  deploy: {
    env: 'production',
  },
  skipEnvironmentCheck: true,
  sourceMaps: {
    include: ['./dist/assets'],
    ignore: ['node_modules'],
    urlPrefix: '~/assets',
  },
};

export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
    process.env.NODE_ENV === 'production' ? viteSentry(sentryConfig) : null,
  ],
  build: {
    sourcemap: process.env.NODE_ENV === 'production',
  },
  server: {
    port: 8080,
    host: '127.0.0.1',
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8856',
        changeOrigin: true,
      }
    }
  }
});