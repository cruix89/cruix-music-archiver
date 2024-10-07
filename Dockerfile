FROM debian:11-slim

ENV S6_BEHAVIOUR_IF_STAGE2_FAILS="2" \
    PUID="911" \
    PGID="911" \
    UMASK="022" \
    OPENSSL_CONF=""

# create group and user
RUN set -x && \
    addgroup --gid "$PGID" abc && \
    adduser --gecos "" --disabled-password --no-create-home --uid "$PUID" --ingroup abc --shell /bin/bash abc

# copy files
COPY root/ /

# install dependencies and packages
RUN set -x && \
    apt update && \
    apt install -y \
        file \
        wget \
        python3 \
        python3-pip \
        libc-dev \
        xvfb \
        scrot \
        imagemagick \
        xclip && \
    python3 -m pip --no-cache-dir install -r /app/requirements.txt && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /app/requirements.txt

# install FFMPEG
RUN set -x && \
    wget -q -O /tmp/ffmpeg.tar.xz 'https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz' || { echo "download failed"; exit 1; } && \
    ls -lh /tmp && \
    tar -xJ -C /tmp/ --one-top-level=ffmpeg && \
    chmod -R a+x /tmp/ffmpeg/* && \
    mv /tmp/ffmpeg/*/ffmpeg /usr/local/bin/ && \
    mv /tmp/ffmpeg/*/ffprobe /usr/local/bin/ && \
    mv /tmp/ffmpeg/*/ffplay /usr/local/bin/ && \
    rm -rf /tmp/*

# install S6 overlay
RUN set -x && \
    wget -q -O /tmp/s6-overlay.tar.gz https://github.com/just-containers/s6-overlay/releases/download/v2.2.0.3/s6-overlay-amd64.tar.gz && \
    tar -xzf /tmp/s6-overlay.tar.gz -C / && \
    rm -rf /tmp/*

# install yt-dlp
RUN set -x && \
    python3 -m pip --no-cache-dir install yt-dlp

# install PhantomJS
RUN set -x && \
    wget -q https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    tar -xf phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    mv phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/bin/phantomjs && \
    rm -rf phantomjs-2.1.1-linux-x86_64 phantomjs-2.1.1-linux-x86_64.tar.bz2

# set volumes and working directory
VOLUME /config /downloads
WORKDIR /config

# entrypoint
ENTRYPOINT ["/init"]