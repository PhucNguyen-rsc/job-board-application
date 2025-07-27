import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const isDev = process.env.NODE_ENV !== 'production';

export default defineConfig({
  base: '/',
  plugins: [react()],
  server: {
    port: 3000,
    strictPort: true,
    host: true,
    cors: isDev
      ? {
          origin: ['http://127.0.0.1:8000'],
          credentials: true,
        }
      : true,
    fs: { strict: true },

    ...(isDev && {
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          const forbidden = ["/.git", "/.hg", "/.bzr", "/.darcs", "/BitKeeper"];
          const fakeStatic = ["/robots.txt", "/sitemap.xml", "/vite.svg"];
          if (forbidden.some((f) => req.url?.startsWith(f))) {
            res.statusCode = 403;
            res.end('Forbidden');
            return;
          }
          if (fakeStatic.includes(req.url)) {
            res.statusCode = 404;
            res.end('Not Found');
            return;
          }

          res.setHeader(
            'Content-Security-Policy',
            [
              "default-src 'self'",
              "script-src 'self'",
              "style-src 'self' 'unsafe-inline'",
              "img-src 'self' data:",
              "font-src 'self'",
              "object-src 'none'",
              "connect-src 'self' http://127.0.0.1:8000",
              "form-action 'self'",
              "frame-ancestors 'self'"
            ].join('; ')
          );

          res.setHeader('X-Frame-Options', 'SAMEORIGIN');
          res.setHeader('Access-Control-Allow-Origin', 'http://127.0.0.1:8000');
          next();
        });
      }
    }),
  },
});
