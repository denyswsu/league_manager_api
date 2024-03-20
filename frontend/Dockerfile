FROM node:20.11

WORKDIR /usr/src/frontend

ENV PATH /usr/src/frontend/node_modules/.bin:$PATH

COPY package*.json ./

RUN npm install

COPY . .

CMD ["vite", "--host"]
