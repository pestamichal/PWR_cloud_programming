FROM node:18-alpine AS builder
WORKDIR /appfront
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
RUN npm prune --production


FROM node:18-alpine
WORKDIR /appfront
COPY --from=builder /appfront/build build/
COPY --from=builder /appfront/node_modules node_modules/
COPY package.json .
ENV PORT 5050
EXPOSE 5050

CMD ["node", "build"]