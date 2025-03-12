FROM swaggerapi/swagger-ui:v5.18.3

# Add files from parser directory
# in host machine to the swagger
# directory.
ADD parser/ /swagger

# Set the environment variables.
ARG APP_NAME
ARG SERVER_HOST
ARG SERVER_PORT
ENV APP_NAME=${APP_NAME}
ENV SERVER_HOST=${SERVER_HOST}
ENV SERVER_PORT=${SERVER_PORT}

WORKDIR /swagger/
# Run script that generates the
# swagger.yml file to be used
# by the Swagger UI container.
RUN node swagger_parser.js
WORKDIR /