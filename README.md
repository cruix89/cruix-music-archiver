
# 🎶 cruix89 / cruix-music-archiver 🎶

[![GitHub last commit](https://img.shields.io/github/last-commit/cruix89/cruix-music-archiver?logo=github)](https://github.com/cruix89/cruix-music-archiver/actions/workflows/push-unstable-image.yml/)
[![GitHub Automated build](https://img.shields.io/github/actions/workflow/status/cruix89/cruix-music-archiver/push-release-version-image.yml?logo=github)](https://github.com/cruix89/cruix-music-archiver/actions/workflows/push-release-version-image.yml/)
[![Image Size](https://img.shields.io/docker/image-size/cruix89/cruix-music-archiver/latest?style=flat&logo=docker)](https://hub.docker.com/r/cruix89/cruix-music-archiver/)
[![Docker Pulls](https://img.shields.io/docker/pulls/cruix89/cruix-music-archiver?style=flat&logo=docker)](https://hub.docker.com/r/cruix89/cruix-music-archiver/)
[![Docker Stars](https://img.shields.io/docker/stars/cruix89/cruix-music-archiver?style=flat&logo=docker)](https://hub.docker.com/r/cruix89/cruix-music-archiver/)

---

## 🎼 OVERVIEW
a fully automated `yt-dlp` docker image to easily download and manage a music library based in YouTube Music and other supported music platforms by `yt-dlp`.

---

📌 docker hub: [cruix-music-archiver](https://hub.docker.com/r/cruix89/cruix-music-archiver)  
📄 yt-dlp documentation: [yt-dlp](https://github.com/yt-dlp/yt-dlp)

---

## ✨ FEATURES

- **simple setup & usage**  
  default settings for optimal operation configured automatically.
  
- **automatic updates**  
  self-updating container with automatic image creation with each `yt-dlp` release.
  
- **automated downloads**  
  specify a download URL file, and easily manage permissions to download every new release from your favorite artists.

- **yt-dlp customization**  
  includes support for SponsorBlock, Geo Bypass, Proxy, Metadata, and more.

---

## 🚀 QUICK START

"download music from `artists.txt` URL file:"

```bash
docker run
  -d
  --name='cruix-music-archiver'
  --privileged=true
  -e TZ="America/Sao_Paulo"
  -e 'youtubedl_interval'='1h'
  -e 'PUID'='1000'
  -e 'PGID'='100'
  -e 'UMASK'='000'
  -v 'PATH':'/config':'rw'
  -v 'PATH':'/downloads':'rw'
  -v 'PATH':'/music':'rw' 'cruix89/cruix-music-archiver'
```

---

## 🔧 ENVIRONMENT PARAMETERS

| Parameter             | Default           | Description                                                      |
|-----------------------|-------------------|------------------------------------------------------------------|
| `TZ`                  |`America/Sao_Paulo`| set time zone for accurate log timestamps.                       |
| `PUID`                | `1000`            | specify user ID for file permissions.                            |
| `PGID`                | `100`             | specify group ID for file permissions.                           |
| `UMASK`               | `000`             | set UMASK for file permissions.                                  |
| `youtubedl_interval`  | `1h`              | set download interval, e.g., `1h`, `12h`, or `false` to disable. |

---

## 🏷️ IMAGE TAGS

- **`unstable`**: built on new 🐙 GitHub commits; updates `yt-dlp` to latest commit.
- **`latest`**: built on new `yt-dlp` releases; auto-updates during runtime.
- **`v<VERSION>`**: built on `yt-dlp` release; does not auto-update.

---

## 📂 CONFIGURATION

- **artists.txt**  
  location: `/config/artists.txt`. artist list or playlist URLs to download.
  
  adding a new link by txt editing:
  ```plaintext
  # ONE URL PER LINE
  https://music.youtube.com/channel/UC2DXTFA6ACS0Qb9QtFlAVDg
  ```
  adding a new link by docker command:
  ```plaintext
  docker exec youtube-dl bash -c 'echo "URL" >> ./artists.txt'
  ```

- **pre-execution.sh / post-execution.sh**  
  these are the scripts that run before and after downloads to process and manage the music library.

- **archive.txt**  
  records downloaded music IDs, delete to re-download all.

- **args.conf**  
  stores `yt-dlp` arguments, customizable for different needs.

For more `yt-dlp` options, check the [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp#usage-and-options).