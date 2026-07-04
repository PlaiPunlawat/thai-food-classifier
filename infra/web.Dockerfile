FROM node:22-alpine AS builder

WORKDIR /app

RUN corepack enable pnpm

COPY pnpm-workspace.yaml package.json pnpm-lock.yaml ./
COPY apps/web/package.json ./apps/web/
COPY packages/ ./packages/

RUN pnpm install --frozen-lockfile

COPY apps/web/ ./apps/web/

ARG NEXT_PUBLIC_API_ENDPOINT=http://localhost:5000/api
ARG NEXT_PUBLIC_PUBLIC_BASE_URL=http://localhost:3000
ENV NEXT_PUBLIC_API_ENDPOINT=$NEXT_PUBLIC_API_ENDPOINT
ENV NEXT_PUBLIC_PUBLIC_BASE_URL=$NEXT_PUBLIC_PUBLIC_BASE_URL

RUN pnpm --filter web build

FROM node:22-alpine

WORKDIR /app

RUN corepack enable pnpm

COPY pnpm-workspace.yaml package.json pnpm-lock.yaml ./
COPY apps/web/package.json ./apps/web/
COPY packages/ ./packages/

RUN pnpm install --frozen-lockfile --prod

COPY --from=builder /app/apps/web/.next ./apps/web/.next
COPY --from=builder /app/apps/web/public ./apps/web/public
COPY --from=builder /app/apps/web/next.config.js ./apps/web/next.config.js

EXPOSE 3000

CMD ["pnpm", "--filter", "web", "start"]
