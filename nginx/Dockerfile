FROM nginx:alpine

# Copy custom config
COPY default.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf

# Create required directories with proper permissions
RUN mkdir -p /var/cache/nginx /var/run \
    && chown -R nginx:nginx /var/cache/nginx /var/run /etc/nginx/conf.d

# Health check: ensure Nginx is serving HTTP
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --spider --quiet http://localhost:8080 || exit 1

# Run as non-root for security
USER nginx
