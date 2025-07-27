FROM alpine:3.21

# Install dependencies 
RUN apk update && apk add --no-cache python3-dev py3-pip curl

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set up app directory
WORKDIR /app
COPY requirements.txt .

# Create and activate virtual environment properly
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Set permissions
RUN chmod +x gunicornstarter.sh
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

EXPOSE 8000

# Add HEALTHCHECK 
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8000/ || exit 1

ENTRYPOINT ["sh", "./gunicornstarter.sh"]
