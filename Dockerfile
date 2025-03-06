FROM debian:12-slim

ENV S6_BEHAVIOUR_IF_STAGE2_FAILS="2" \
    PUID="911" \
    PGID="911" \
    UMASK="022" \
    OPENSSL_CONF=""

# create group and user
RUN addgroup --gid "$PGID" abc && \
    adduser --gecos "" --disabled-password --uid "$PUID" --ingroup abc --shell /bin/bash abc

# install dependencies and packages
RUN apt update && apt install -y \
        supervisor \
        file \
        wget \
        curl \
        ca-certificates \
        python3 \
        python3-pip \
        python3-importlib-metadata \
        python3-certifi \
        python3-brotli \
        python3-pycryptodome \
        python3-eyed3 \
        python3-mutagen \
        python3-requests \
        python3-pylast \
        python3-pillow \
        libffi-dev \
        libgmp-dev \
        libbrotli-dev \
        gnupg \
        ffmpeg \
        gosu \
        libjpeg-dev \
        zlib1g-dev \
        libpng-dev \
        libtiff-dev \
        liblcms2-dev \
        libffi-dev \
        libgdk-pixbuf2.0-dev \
        libmagickwand-dev \
        imagemagick && \
    apt clean && rm -rf /var/lib/apt/lists/*

# install using pip3
RUN pip3 --no-cache-dir install --break-system-packages beautifulsoup4
RUN pip3 --no-cache-dir install --break-system-packages yt-dlp

# copy remaining files
COPY root/ /

# install S6 overlay
RUN wget -q -O /tmp/s6-overlay.tar.gz https://github.com/just-containers/s6-overlay/releases/download/v2.2.0.3/s6-overlay-amd64.tar.gz && \
    tar -xzf /tmp/s6-overlay.tar.gz -C / && \
    rm -rf /tmp/*

# set volumes and working directory
VOLUME /config /downloads /music
WORKDIR /config

# entrypoint
ENTRYPOINT ["/init"]