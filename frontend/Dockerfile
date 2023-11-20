FROM node:20

WORKDIR /app

COPY . .

RUN npm ci
RUN npm run build

CMD node build/index.js
