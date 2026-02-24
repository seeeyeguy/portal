FROM python:3.12-bullseye AS base

# Add needed env variables.
ARG APP_NAME
ARG CA_CERTIFICATE_FOR_API

# Construct path to project.
# Need to change PROJECT to app name.
ARG PROJECT=${APP_NAME}
ARG APPDIR=/apps/${PROJECT}

# Add project to python path.
ENV PYTHONPATH ${APPDIR}
# Send container output to stdout.
ENV PYTHONUNBUFFERED 1

ADD ${CA_CERTIFICATE_FOR_API} /usr/local/share/${CA_CERTIFICATE_FOR_API}
ADD ${CA_CERTIFICATE_FOR_API} /usr/local/share/ca-certificates/internal-ca.crt
RUN update-ca-certificates
ENV PIP_CERT=/usr/local/share/${CA_CERTIFICATE_FOR_API}

# Install container dependencies.
RUN DevTools="emacs iputils-ping less netcat openssh-client unzip vim zip" && \
    TLSDeps="apt-transport-https ca-certificates gnupg1 libsasl2-dev libssl-dev" && \
    PostgresDeps="gcc libpq-dev postgresql-client python3-dev" && \
    MSSQLDeps="msodbcsql17 unixodbc" && \
    DjangoDeps="cron graphviz graphviz-dev libjpeg-dev python3-enchant" && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc && \
    curl https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/msprod.list && \
    curl -sSL -O https://packages.microsoft.com/config/debian/11/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb && \
    apt clean all && \
    apt --allow-releaseinfo-change update && \
    apt dist-upgrade -y && \
    ACCEPT_EULA=Y apt install --fix-missing -y $DevTools $TLSDeps $PostgresDeps $DjangoDeps $MSSQLDeps && \
    pip install --upgrade pip && \
    apt autoremove -y

# Change current working directory
# to app directory. 
WORKDIR ${APPDIR}

# Upgrade pip and install app dependencies.
ADD requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Override library code to fix errors.
ADD ./packages/rest_framework/parsers.py /usr/local/lib/python3.9/site-packages/rest_framework/parsers.py

ADD init.sh /apps/init.sh
ADD entrypoint.sh /apps/entrypoint.sh
RUN chmod +x /apps/init.sh
RUN chmod +x /apps/entrypoint.sh


#
#   DEVELOPMENT BUILD SPECIFICATION
#


# From the base build, build development
# container.
FROM base AS development

# Install sudo.
RUN apt install sudo

# Install dev dependencies.
ADD requirements.dev.txt .
RUN pip install -r requirements.dev.txt && \
    rm -f requirements.*

# Configure user.
ARG USER
ARG UID
ARG PASSWORD
RUN useradd --create-home --shell /bin/bash -u $UID -G users,sudo,root $USER && \
    mkdir -p /home/$USER/.ssh/ && \
    chown $USER:users /home/$USER/.ssh/ && \
    echo $USER:$PASSWORD | chpasswd

USER $USER
ENV HOME /home/$USER

# Run api service.
ENTRYPOINT [ "/apps/entrypoint.sh" ]


#
#   WSGI DEVELOPMENT
#

FROM development AS wsgi-development

EXPOSE 8080
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8080"]

#
#   ASGI DEVELOPMENT
#

FROM development AS asgi-development

EXPOSE 8080
CMD [ "python", "-m", "uvicorn", "manager.asgi:application", "--host", "0.0.0.0", "--port", "8080", "--reload", "--reload-include", "*.*"]

#
#   PRODUCTION BUILD SPECIFICATION
#


# From the base build, build production
# container.
FROM base AS production

RUN rm -f requirements.*

ADD src/ ${APPDIR}

ENTRYPOINT ["/apps/entrypoint.sh"]


#
#   WSGI PRODUCTION
#

FROM production AS wsgi-production

EXPOSE 8080
CMD ["gunicorn", "--bind", ":8080", "--workers", "8", "manager.wsgi:application"]

#
#   ASGI PRODUCTION
#

FROM production AS asgi-production

EXPOSE 8080
CMD ["gunicorn", "--bind", ":8080", "--workers", "8", "-k", "uvicorn_worker.UvicornWorker", "manager.asgi:application"]
