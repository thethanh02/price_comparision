# FROM node:18-alpine3.17 as build

# WORKDIR /app
# COPY . /app

# RUN npm install
# RUN npm run build

# FROM ubuntu
# RUN apt-get update
# RUN apt-get install nginx -y
# COPY --from=build /app/dist /var/www/html/
# EXPOSE 80
# CMD ["nginx","-g","daemon off;"]

FROM node:18-alpine3.17
WORKDIR /app
COPY . .
RUN yarn
EXPOSE 5173
CMD ["yarn", "dev", "--host", "0.0.0.0"]