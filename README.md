
# 🎶 cruix89 / cruix-music-archiver 🎶

[![GitHub last commit](https://img.shields.io/github/last-commit/cruix89/cruix-music-archiver?logo=github)](https://github.com/cruix89/cruix-music-archiver/actions/workflows/push-unstable-image.yml/)
[![GitHub Automated build](https://img.shields.io/github/actions/workflow/status/cruix89/cruix-music-archiver/push-release-version-image.yml?logo=github)](https://github.com/cruix89/cruix-music-archiver/actions/workflows/push-release-version-image.yml/)
[![Image Size](https://img.shields.io/docker/image-size/cruix89/cruix-music-archiver/latest?style=flat&logo=docker)](https://hub.docker.com/r/cruix89/cruix-music-archiver/)
[![Docker Pulls](https://img.shields.io/docker/pulls/cruix89/cruix-music-archiver?style=flat&logo=docker)](https://hub.docker.com/r/cruix89/cruix-music-archiver/)
[![Docker Stars](https://img.shields.io/docker/stars/cruix89/cruix-music-archiver?style=flat&logo=docker)](https://hub.docker.com/r/cruix89/cruix-music-archiver/)

## 🎼 OVERVIEW
a fully automated `yt-dlp` docker image to easily download and manage a music library based in YouTube Music and other supported music platforms by `yt-dlp`.

📌 Docker Hub: [cruix-music-archiver](https://hub.docker.com/r/cruix89/cruix-music-archiver)  
📄 yt-dlp Documentation: [yt-dlp](https://github.com/yt-dlp/yt-dlp)

---

## ✨ Features

- **Simple Setup & Usage**  
  Configure audio quality, format, and startup arguments via environment variables.
  
- **Automatic Updates**  
  Self-updating container with automatic image builds.
  
- **Automated Downloads**  
  Specify download intervals, use URL files, and manage permissions easily.

- **yt-dlp Customization**  
  Includes support for SponsorBlock, Geo bypass, Proxy, Metadata, and more.

---

## 🚀 Quick Start

"Download music from `artists.txt` URL file:"

```bash
docker run -d --name='cruix-music-archiver' --privileged=true \
  -e TZ="America/Sao_Paulo" -e 'youtubedl_interval'='1h' -e 'PUID'='1000' \
  -e 'PGID'='100' -e 'UMASK'='000' -v '/config':'/config':'rw' \
  -v '/downloads':'/downloads':'rw' -v '/music':'/music':'rw' \
  cruix89/cruix-music-archiver
```

---

## 🔧 Environment Parameters

| Parameter             | Default           | Description                                                       |
|-----------------------|-------------------|-------------------------------------------------------------------|
| `TZ`                  |`America/Sao_Paulo`| Set time zone for accurate log timestamps.                        |
| `PUID`                | `1000`            | Specify user ID for file permissions.                             |
| `PGID`                | `100`             | Specify group ID for file permissions.                            |
| `UMASK`               | `000`             | Set umask for file permissions.                                   |
| `youtubedl_interval`  | `1h`              | Set download interval, e.g., `1h`, `12h`, or `false` to disable.  |

---

## 🏷️ Image Tags

- **`unstable`**: Built on new GitHub commits; updates `yt-dlp` to latest commit.
- **`latest`**: Built on new `yt-dlp` releases; auto-updates during runtime.
- **`v<VERSION>`**: Built on `yt-dlp` release; does not auto-update.

---

## 📂 Configuration

- **artists.txt**  
  Location: `/config/artists.txt`. List artist or playlist URLs to download.
  
  ```plaintext
  # One URL per line
  https://music.youtube.com/channel/UC2DXTFA6ACS0Qb9QtFlAVDg
  ```

- **pre-execution.sh / post-execution.sh**  
  Optional user-defined scripts executed before and after downloads.

- **archive.txt**  
  Records downloaded music IDs. Delete to re-download all.

- **args.conf**  
  Stores `yt-dlp` arguments, customizable for different needs.

For more `yt-dlp` options, check the [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp#usage-and-options).