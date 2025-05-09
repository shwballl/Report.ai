FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# Serve using Nginx
FROM nginx:1.16.0-alpine

COPY --from=build /app/dist /usr/share/nginx/html
