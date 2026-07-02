FROM lsiobase/alpine:3.24
LABEL maintainer="xcxxcxcxz"

WORKDIR /geoip2influx

# Copy the requirements.txt and run.py files
COPY requirements.txt run.py ./

# Copy the entire geoip2influx directory
COPY /geoip2influx /geoip2influx/

RUN \
  echo " ## Runtime Packages ## " && \
  apk add --no-cache \
    python3 \
    logrotate \
    libmaxminddb && \
  \
  echo " Build-only Packages ## " && \
  apk add --no-cache --virtual .build-deps \
    py3-pip \
    build-base \
    python3-dev && \
  \
  echo " ## Python  ## " && \
  python3 -m venv /lsiopy && \
  /lsiopy/bin/pip install --no-cache-dir -U pip setuptools wheel && \
  /lsiopy/bin/pip install --no-cache-dir -r requirements.txt && \
  \
  echo " ## Clean ## " && \
  apk del .build-deps
  
COPY root/ /
