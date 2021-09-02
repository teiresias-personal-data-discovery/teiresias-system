# build
FROM node:15 as builder
RUN mkdir /service
WORKDIR /service
COPY . .
RUN yarn
RUN yarn build

FROM node:15-alpine
RUN mkdir /service
WORKDIR /service
COPY --from=builder /service .
CMD ["yarn", "start:prod"]