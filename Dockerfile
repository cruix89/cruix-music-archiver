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
    apt install --no-install-recommends -y \
        file \
        wget \
        python3 \
        python3-pip \
        libc-dev \
        xvfb \
        scrot \
        imagemagick \
        xclip \
        curl \
        ca-certificates \
        fonts-liberation \
        libappindicator3-1 \
        libasound2 \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libcups2 \
        libdbus-1-3 \
        libdrm2 \
        libgbm1 \
        libgtk-3-0 \
        libnspr4 \
        libnss3 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        xdg-utils \
        gnupg \
        nodejs \
        npm && \
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

# install chrome
RUN set -x && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt update && \
    apt install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# install puppeteer
RUN set -x && \
    npm install -g puppeteer && \
    ln -s /usr/bin/google-chrome-stable /usr/bin/google-chrome

# install S6 overlay
RUN set -x && \
    wget -q -O /tmp/s6-overlay.tar.gz https://github.com/just-containers/s6-overlay/releases/download/v2.2.0.3/s6-overlay-amd64.tar.gz && \
    tar -xzf /tmp/s6-overlay.tar.gz -C / && \
    rm -rf /tmp/*

# install yt-dlp
RUN set -x && \
    python3 -m pip --no-cache-dir install yt-dlp

# set volumes and working directory
VOLUME /config /downloads
WORKDIR /config

# entrypoint
ENTRYPOINT ["/init"]