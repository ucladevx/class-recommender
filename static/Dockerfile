FROM node:latest
MAINTAINER Jesse Cai <jcjessecai@gmail.com>

# install npm and node
RUN apt-get update -y && apt-get install -y nginx

# nginx config
COPY ./nginx/default.conf /etc/nginx/nginx.conf

# Prepare app directory
RUN mkdir -p /static

# cache so npm install doesn't take ages every time
ADD package.json /static/package.json
RUN cd /static && npm install

ADD . /static

WORKDIR /static
RUN npm run build

RUN mkdir -p public && mkdir -p public/build
RUN cp -r pages/* public && cp lib/build/main.css public/build && cp lib/build/main.js public/build

WORKDIR /static/public
# Expose the app port
EXPOSE 80

# Start the app
CMD ["nginx", "-g", "daemon off;"]
