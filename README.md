
# 🎶 cruix89 / cruix-music-archiver 🎶

[![GitHub last commit](https://img.shields.io/github/last-commit/cruix89/cruix-music-archiver?logo=github)](https://github.com/cruix89/cruix-music-archiver/actions/workflows/push-unstable-image.yml/)
[![GitHub Automated build](https://img.shields.io/github/actions/workflow/status/cruix89/cruix-music-archiver/push-release-version-image.yml?logo=github)](https://github.com/cruix89/cruix-music-archiver/actions/workflows/push-release-version-image.yml/)
[![Image Size](https://img.shields.io/docker/image-size/cruix89/cruix-music-archiver/latest?style=flat&logo=docker)](https://hub.docker.com/r/cruix89/cruix-music-archiver/)
[![Docker Pulls](https://img.shields.io/docker/pulls/cruix89/cruix-music-archiver?style=flat&logo=docker)](https://hub.docker.com/r/cruix89/cruix-music-archiver/)
[![Docker Stars](https://img.shields.io/docker/stars/cruix89/cruix-music-archiver?style=flat&logo=docker)](https://hub.docker.com/r/cruix89/cruix-music-archiver/)

---

## 🎼: OVERVIEW
a fully automated `yt-dlp` docker image to easily download and manage a music library based in YouTube Music and other supported music platforms by `yt-dlp`.

---

## 💖 Support This Project

if you find this project useful, consider buy me a coffee 😊:

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub-%23EA4AAA?style=for-the-badge&logo=github)](https://github.com/cruix89/cruix-music-archiver/sponsor)

THANK YOU! for your support! 😊

📌 docker hub: [cruix-music-archiver](https://hub.docker.com/r/cruix89/cruix-music-archiver)  
📄 yt-dlp documentation: [yt-dlp](https://github.com/yt-dlp/yt-dlp)

---

## ✨: FEATURES

- **simple setup & usage**  
  default settings for optimal operation configured automatically.
  
- **automatic updates**  
  self-updating container with automatic image creation with each `yt-dlp` release.
  
- **automated downloads**  
  specify a download URL file, and easily manage permissions to download every new release from your favorite artists.

- **yt-dlp customization**  
  includes support for SponsorBlock, Geo Bypass, Proxy, Metadata, and more.

- **smart caches and config files**  
  folders, cache and configuration files in the /config directory for full control of execution processes.

---

## 🚀: QUICK START

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

## 🔧: ENVIRONMENT PARAMETERS

| Parameter            | Default             | Description                                                      |
|----------------------|---------------------|------------------------------------------------------------------|
| `TZ`                 | `America/Sao_Paulo` | set time zone for accurate log timestamps.                       |
| `PUID`               | `1000`              | specify user ID for file permissions.                            |
| `PGID`               | `100`               | specify group ID for file permissions.                           |
| `UMASK`              | `000`               | set UMASK for file permissions.                                  |
| `youtubedl_interval` | `1h`                | set download interval, e.g., `1h`, `12h`, or `false` to disable. |

---

## 🏷️: IMAGE TAGS

- **`unstable`**: built on new 🐙 GitHub commits; updates `yt-dlp` to latest commit.
- **`latest`**: built on new `yt-dlp` releases; auto-updates during runtime.
- **`v<VERSION>`**: built on `yt-dlp` release; does not auto-update.

---

## 📂: CONFIGURATION

- **cache folder**  
  temporary directory where files are processed, the script automatically cleans the directory. 


- **dz-db folder**  
  music information database directory, the database is updated with each script run. 


- **logs folder**  
  all system logs are stored in this directory and restarted with each run for better space and process control.


- **recycle-bin folder**  
  directory where unnecessary thumbnails and corrupted files are moved. The directory stores files for 7 days, check the files you want to check within this period.

  
- **unofficial-albums folder**  
  this directory stores albums and playlists added to the artist that are not official. The directory stores the albums for 7 days, if you wish, you can retrieve the albums and manually move them to your library within this period. 
  **ATTENTION:** if you save the albums to your library, move them to a folder other than /music , because if you do, the unofficial album will be moved again to the unofficial albums directory the next time the script is run.


- **archive.txt**  
  records downloaded music IDs, delete to re-download all.


- **args.conf**  
  stores `yt-dlp` arguments, customizable for different needs.


- **artists.txt**  
  location: `/config/artists.txt`. artist list or playlist URLs to download.
  
  adding a new link by .txt editing:
  ```plaintext
  # ARTIST NAME
  https://music.youtube.com/channel/UCkrV3aukHg-BB2xT8D3Hwyw
  ```
  adding a new link by docker command:
  ```plaintext
  docker exec youtube-dl bash -c 'echo "# ARTIST NAME" >> ./artists.txt'
  docker exec youtube-dl bash -c 'echo "https://music.youtube.com/channel/UCkrV3aukHg-BB2xT8D3Hwyw" >> ./artists.txt'
  ```

- **genres_cache.txt**  
  this cache is built through an API and applied to the artist's musical style. If you do not agree with the information provided by the api, you can modify the .txt file and apply what you think is correct and the system will apply the artist genre tag to whatever is contained in the cache file without overwriting what was changed.


- **loudnorm_cache.txt**  
  this cache file stores the files already processed by ffmpeg, if you want to reprocess your library, delete this file.


- **loudnorm_failed_files_cache.txt**  
  this cache stores library files that were corrupted and removed by the system. If this file appears in your /config, examine the files and add another link to download the file again if you want.


- **post-execution.sh**  
  these are the script that run before and after downloads to process and manage the music library.

---

## ❌:  EXCEPTIONS

- **unsupported arguments**
 ```plaintext
  --config-location, hardcoded to /config/args.conf.
  --batch-file, hardcoded to /config/channels.txt.
  ```
  
---

## ⚙️:  DEFAULTS

- **default arguments**

| Parameter                | Default                                                | Description                                                           |
|--------------------------|--------------------------------------------------------|-----------------------------------------------------------------------|
| `--output`               | `"/downloads/%(channel)s/%(album)s/%(title)s.%(ext)s"` | organize the download directory by "/artist/album/song"               |
| `--parse-metadata`       | `"channel:%(album_artist)s"`                           | adds the "album artist" tag if it doesn't exist in the song           |
| `--format`               | `bestaudio`                                            | download the best possible audio quality                              |
| `--force-overwrites`     | `--force-overwrites`                                   | prevents duplicate songs for the same album                           |
| `--windows-filenames`    | `--windows-filenames`                                  | writes files with compatibility for windows system                    |
| `--trim-filenames`       | `260`                                                  | maximum filename length                                               |
| `--newline`              | `--newline`                                            | logs each download progress on a line separately for better debugging |
| `--progress`             | `--progress`                                           | debug download progress                                               |
| `--write-all-thumbnails` | `--write-all-thumbnails`                               | saves all thumbnail formats so the code can select the best one       |
| `--extract-audio`        | `--extract-audio`                                      | send the audio extraction command                                     |
| `--audio-format`         | `flac`                                                 | download without loss of quality format                               |
| `--embed-metadata`       | `--embed-metadata`                                     | writes metadata to file                                               |
| `--sleep-requests`       | `1.5`                                                  | waits for time to prevent request blocking                            |
 
---

for more `yt-dlp` options, check the [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp#usage-and-options).