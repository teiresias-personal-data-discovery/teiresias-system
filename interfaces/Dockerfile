FROM node:15-alpine as builder
RUN mkdir /service
WORKDIR /service
COPY . .
RUN yarn --production 
ARG REACT_APP_INVENTORYAPI_BASE
ARG REACT_APP_AIRFLOW_BASE
ARG REACT_APP_FLOWER_BASE
RUN yarn build

FROM nginx:stable-alpine
COPY --chown=nginx:nginx --from=builder /service/build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY --chown=nginx:nginx server/nginx.conf /etc/nginx/conf.d
CMD ["nginx", "-g", "daemon off;"]
