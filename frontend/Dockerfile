# Build stage
FROM node:23-alpine AS build

WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build  # ✅ Fixed typo

# Final Nginx serving stage
FROM nginx:alpine

# Copy built assets to Nginx's HTML folder
COPY --from=build /app/dist /usr/share/nginx/html

# Create a custom Nginx configuration file
RUN mkdir -p /etc/nginx/conf.d
COPY nginx.conf /etc/nginx/nginx.conf

# Create required directories with proper permissions
RUN mkdir -p /var/cache/nginx /var/run \
    && chown -R nginx:nginx /var/cache/nginx /var/run /usr/share/nginx/html /etc/nginx/conf.d

# ✅ Add HEALTHCHECK (adjust endpoint if needed)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080 || exit 1

# Use non-root user
USER nginx

# Nginx will listen on this port
EXPOSE 8080
