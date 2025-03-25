/// <reference types="vitest/config" />
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";

// Shared config settings.
const SHARED = {
  host: "0.0.0.0",
  proxy: {
    "/api": {
      target: "http://api:8080",
      changeOrigin: true,
      secure: false,
      rewrite: (path: string) => path.replace(/^\/api/, ""),
    },
  },
};

// https://vitejs.dev/config/
export default defineConfig({
  define: {
    __APP_NAME__: JSON.stringify(process.env.APP_NAME),
    __APP_TITLE__: JSON.stringify(process.env.APP_TITLE),
    __DATA_ENCRYPTION_KEY__: JSON.stringify(process.env.DATA_ENCRYPTION_KEY),
    __SCHEME__: JSON.stringify(process.env.SCHEME),
    __WEB_HOST__: JSON.stringify(process.env.WEB_HOST),
    __WEB_PORT__: JSON.stringify(process.env.WEB_PORT),
  },
  plugins: [react(), tsconfigPaths()],
  test: {
    globals: true,
    environment: "jsdom",
    pool: "vmThreads",
    setupFiles: ["./vitest.setup.ts"],
  },
  preview: {
    ...SHARED,
    port: 3001,
  },
  server: {
    ...SHARED,
    port: 3000,
  },
});
