# Single-stage build for Node.js JavaScript
FROM node:20-slim

WORKDIR /app

ENV NODE_ENV=production

# Install dependencies first (layer caching)
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev

# Copy application source
COPY src/ ./src/

EXPOSE 3000

CMD ["node", "src/index.js"]
