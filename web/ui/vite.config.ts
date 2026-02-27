/// <reference types="vitest/config" />
import fs from "node:fs";
import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";



// Read in certificates from SSL Directory and set up HTTPS if found.
function getSslOptions() {
  const sslDir = process.env.SSL_DIRECTORY ?? "";
  const sslCert = process.env.SSL_CERT ?? "";
  const sslKey = process.env.SSL_KEY ?? "";
  const sslPass = process.env.SSL_PASS ?? "";

  const certPath = path.join(sslDir, sslCert);
  const keyPath = path.join(sslDir, sslKey);
  const passPath = path.join(sslDir, sslPass);

  if (
    !fs.existsSync(certPath) ||
    !fs.lstatSync(certPath).isFile() ||
    !fs.existsSync(keyPath) ||
    !fs.lstatSync(keyPath).isFile()
  ) {
    console.warn(
      `[vite] SSL certificate or key not found in ${sslDir}, HTTPS will be disabled.`
    );
    return undefined;
  }

  console.info(
    `[vite] SSL files found in ${sslDir}. HTTPS will be enabled.`, 
  );

  const httpsOptions: { cert: Buffer; key: Buffer; passphrase?: string } = {
    cert: fs.readFileSync(certPath),
    key: fs.readFileSync(keyPath),
  };

  if (sslPass && fs.existsSync(passPath) && fs.lstatSync(passPath).isFile()) {
    httpsOptions.passphrase = fs.readFileSync(passPath, "utf8").trim();
  } else if (sslPass) {
    console.warn(
      `[vite] SSL passphrase file not found or not a regular file: ${passPath}`
    );
  }

  return httpsOptions;
}

// Shared config settings.
export const SHARED = {
  host: "0.0.0.0",
  proxy: {
    "/api": {
      target: "http://api:8080",
      changeOrigin: true,
      secure: false,
      rewrite: (path: string) => path.replace(/^\/api/, ""),
    },
    "/v1/svc/sso": {
      target: "http://api:8080",
      changeOrigin: true,
      secure: false,
    },
    "/v1/svc/ldap": {
      target: "http://api:8080",
      changeOrigin: true,
      secure: false,
    },
  },
  allowedHosts: [
    process.env.WEB_HOST as string,
    // Add other allowed hosts if needed
  ],
};

// https://vitejs.dev/config/
export default defineConfig({
  define: {
    __APP_NAME__: JSON.stringify(process.env.APP_NAME),
    __APP_TITLE__: JSON.stringify(process.env.APP_TITLE),
    __DATA_ENCRYPTION_KEY__: JSON.stringify(process.env.DATA_ENCRYPTION_KEY),
    __PROGRAM_REVIEW_EXPORT_CACHE_TIMEOUT_SECONDS__:
      Number(process.env.PROGRAM_REVIEW_EXPORT_CACHE_TIMEOUT_SECONDS) > 0
        ? Number(process.env.PROGRAM_REVIEW_EXPORT_CACHE_TIMEOUT_SECONDS)
        : 3600,
    __SCHEME__: JSON.stringify(process.env.SCHEME),
    __SERVER_PORT__: JSON.stringify(process.env.SERVER_PORT),
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
    https: getSslOptions(), 
  },
});
