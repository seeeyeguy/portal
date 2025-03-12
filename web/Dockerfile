FROM node:20.16-bullseye AS base

# Add needed env variables.
ARG APP_NAME
ARG DATA_ENCRYPTION_KEY
ARG SCHEME
ARG WEB_HOST
ARG WEB_PORT
# Construct path to project.
# Need to change PROJECT to app name.
ARG PROJECT=${APP_NAME}
ARG APPDIR=/apps/${PROJECT}

# Change current working directory
# to app directory.
WORKDIR ${APPDIR}

#
#   DEVELOPMENT BUILD SPECIFICATION
#

FROM base AS development

EXPOSE 3000
CMD ["npm", "run", "dev"]

#
#   PRODUCTION BUILD SPECIFICATION
#

# Nginx is the base build for
# production but we need an intermediate
# step to create the production build for
# the web app. 
FROM base AS builder

ADD ./ui/ .
RUN mkdir -p ${APPDIR}/storage
RUN npm ci && \
    npm run build

###
### Build Stage #2 -- Copy App into Server Image
###

FROM nginx:1.27-alpine AS production

# We need to declare these here again as
# nginx does not inherit from the
# base build.
ARG APP_NAME
ARG PROJECT=${APP_NAME}
ARG APPDIR=/apps/${PROJECT}

COPY --from=builder ${APPDIR}/dist /var/www
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx/conf/template/nginx.conf.template /etc/nginx/templates/nginx.conf.template
EXPOSE 443

