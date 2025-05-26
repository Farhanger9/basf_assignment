# ---------- build stage ----------
FROM node:18 AS builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --silent
COPY frontend ./
RUN npm run build

# ---------- run stage ----------
FROM nginx:1.25-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
