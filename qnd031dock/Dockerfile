FROM python:3.11-alpine
LABEL maintainer="support@smartquail.io"

ENV PYTHONUNBUFFERED=1
ENV NODE_VERSION=qnd031app
ENV NODE_APP_NAME=qnd031app
ENV USER=qnd111
ENV VERSION=111

# Instalar git para clonar el repositorio
RUN apk add --no-cache git

# Argumentos para git clone
ARG username=smartquailDev
ARG password=ms1719183830
RUN git clone https://github.com/smartquailstage/${NODE_VERSION}.git

# Copiar archivos al contenedor
COPY ./${VERSION}.txt /${VERSION}.txt
COPY ./dbb/BDDPSP.csv /${NODE_VERSION}/${NODE_APP_NAME}/BDDPSP.csv
COPY ./scripts /scripts
COPY ./uwsgi_pro.ini /${NODE_VERSION}/${NODE_APP_NAME}/uwsgi_pro.ini
COPY ./qnode_ascii-art.txt /${NODE_VERSION}/${NODE_APP_NAME}/qnode_art.txt

WORKDIR /${NODE_VERSION}/${NODE_APP_NAME}
EXPOSE 9000

# Crear entorno virtual, instalar dependencias, usuario, y configurar sistema
RUN python3.11 -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps && \
    apk add build-base curl postgresql-dev gcc musl-dev python3-dev linux-headers && \
    apk add libffi-dev py3-cffi py3-cryptography jpeg-dev go zlib-dev libjpeg wget && \
    apk --update --upgrade --no-cache add fontconfig ttf-freefont font-noto terminus-font && \
    apk add gtk+3.0 pango busybox-extras openssl-dev gettext && \
    /py/bin/pip install -r /${VERSION}.txt && \
    apk del openssl-dev .tmp-deps && \

    # Crear usuario con UID fijo
    adduser --uid 1000 --disabled-password --no-create-home ${USER} && \

    # Directorios de la app
    mkdir -p /${NODE_VERSION}/${NODE_APP_NAME}/static && \
    mkdir -p /${NODE_VERSION}/${NODE_APP_NAME}/media && \
    mkdir -p /${NODE_APP_NAME}/${NODE_APP_NAME}/staticfiles && \
    chmod -R 755 /${NODE_VERSION}/${NODE_APP_NAME}/static /${NODE_VERSION}/${NODE_APP_NAME}/media /${NODE_APP_NAME}/${NODE_APP_NAME}/staticfiles && \
    chown -R ${USER}:${USER} /${NODE_VERSION}/${NODE_APP_NAME}/media /${NODE_APP_NAME}/${NODE_APP_NAME}/staticfiles /${NODE_VERSION}/${NODE_APP_NAME}/static && \

    # Logs
    mkdir -p /var/log/uwsgi/ /var/log/qnd031app/ && \
    chown -R ${USER}:${USER} /var/log/uwsgi/ /var/log/qnd031app/ && \

    # Fontconfig cache dirs (para evitar errores de fuente)
    mkdir -p /usr/local/share/fonts /etc/fonts /var/cache/fontconfig && \
    chmod -R 755 /usr/local/share/fonts /etc/fonts /var/cache/fontconfig && \
    chown -R ${USER}:${USER} /usr/local/share/fonts /etc/fonts /var/cache/fontconfig && \

    # Permisos scripts
    chmod -R 755 /${NODE_VERSION}/${NODE_APP_NAME}/ && \
    chmod -R 755 /scripts && \
    chown -R ${USER}:${USER} /${NODE_VERSION}/${NODE_APP_NAME}/ /scripts && \
    chmod -R u+x /scripts/uwsgi.sh && \
    chmod -R +x /scripts

# Configuración del entorno
ENV PATH="/py/bin:/scripts:$PATH"

# Zona horaria
RUN apk add --no-cache --update musl musl-utils musl-locales tzdata && \
    cp /usr/share/zoneinfo/America/Guayaquil /etc/localtime

# Localización
RUN echo 'export LC_ALL=es_ES.UTF-8' >> /etc/profile.d/locale.sh && \
    sed -i 's|LANG=C.UTF-8|LANG=es_ES.UTF-8|' /etc/profile.d/locale.sh

ENV LANG=es_ES.UTF-8 \
    LANGUAGE=es_ES.UTF-8

# Usar el usuario sin privilegios
USER ${USER}

# Ejecutar el script uwsgi al iniciar
CMD ["sh", "-c", "uwsgi.sh"]
