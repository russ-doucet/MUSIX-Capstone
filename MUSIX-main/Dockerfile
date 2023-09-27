FROM node:18-alpine as build

ENV NODE_ENV production

#Copy entire folder
COPY ./ /app

#Install npm packages
WORKDIR /app/react-musix
RUN npm install --omit=dev
RUN npm run build --omit=dev

FROM tecktron/python-waitress:latest
ENV VARIABLE_NAME app
ENV MODULE_NAME app

COPY --from=build /app /app

#Install python dependencies
WORKDIR /app
RUN pip install -r requirements.txt

#Move to backend folder before running server
WORKDIR /app/backend
