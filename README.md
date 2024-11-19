
# <img src="https://i.imgur.com/KGjEr5m.png" alt="Logo do Projeto" width="32" height="32"> cruix89 / cruix-music-archiver <img src="https://i.imgur.com/KGjEr5m.png" alt="Logo do Projeto" width="32" height="32">

[![GitHub last commit](https://img.shields.io/github/last-commit/cruix89/cruix-music-archiver?logo=github)](https://github.com/cruix89/cruix-music-archiver/actions/workflows/push-unstable-image.yml/)
[![GitHub Automated build](https://img.shields.io/github/actions/workflow/status/cruix89/cruix-music-archiver/push-release-version-image.yml?logo=github)](https://github.com/cruix89/cruix-music-archiver/actions/workflows/push-release-version-image.yml/)
[![Image Size](https://img.shields.io/docker/image-size/cruix89/cruix-music-archiver/latest?style=flat&logo=docker)](https://hub.docker.com/r/cruix89/cruix-music-archiver/)
[![Docker Pulls](https://img.shields.io/docker/pulls/cruix89/cruix-music-archiver?style=flat&logo=docker)](https://hub.docker.com/r/cruix89/cruix-music-archiver/)
[![Docker Stars](https://img.shields.io/docker/stars/cruix89/cruix-music-archiver?style=flat&logo=docker)](https://hub.docker.com/r/cruix89/cruix-music-archiver/)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-%23FF813F?style=flat&logo=buymeacoffee)](https://buymeacoffee.com/cruix89)


--- 

## 🎼: OVERVIEW
a fully automated `yt-dlp` docker image to easily download and manage a music library based in YT Music and other supported music platforms by `yt-dlp`.

---

## 💖 GENEROSITY

- 😊 **if you like me, consider** [buy me a coffee](https://buymeacoffee.com/cruix89)
- 📌 **docker hub:** [cruix-music-archiver](https://hub.docker.com/r/cruix89/cruix-music-archiver)  
- 📄 **yt-dlp documentation:** [yt-dlp](https://github.com/yt-dlp/yt-dlp)   

---

## ✨: FEATURES

- **simple setup & usage**  
  default settings for optimal operation configured automatically.
  
- **automatic updates**  
  self-updating container with automatic image creation with each `yt-dlp` release.
  
- **automated downloads**  
  specify a download URL file, and easily manage permissions to download.

- **yt-dlp customization**  
  includes support for SponsorBlock, Geo Bypass, Proxy, Metadata, and more.

- **smart caches and config files**  
  folders, cache and configuration files in the /config directory for full control of execution processes.

- **smart tag search engines by apis**  
  genre, missing covers and artist images automatic search engines

- **smart correction and normalization of tags and files**  
  a large library of patches are applied to standardize and correct filenames and tags

- **tracks number correction engine**  
  some songs may have the wrong or missing track numbers. the system uses a solid database to correct the number of tracks

- **unofficial albums and disambiguation**  
  unofficial albums are moved to a specific directory for library cleanup.  
  artists with ambiguous names are correctly renamed by adding valid information using a disambiguation library

- **LUFS-based normalization**  
  audio processing using [ffmpeg](https://github.com/FFmpeg/FFmpeg) to calculate the audio LUFS and normalize the entire library,  
  using the same parameters that major streaming platforms use, improving the sound experience and reducing volume differences between different sounds

- **designed for excellent compatibility with large media center projects**  
  the library structure is organized for great viewing on [plex](https://github.com/plexinc/pms-docker) and [jellyfin](https://jellyfin.org/docs/general/installation/container/)

---

## 🚀: QUICK START

"download music from `artists.txt` URL file:"

```bash
docker run
  -d
  --name='cruix-music-archiver'
  --privileged=true
  -e TZ="America/Sao_Paulo"
  -e 'yt_dlp_interval'='1h'
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
| `yt_dlp_interval` | `1h`                | set download interval, e.g., `1h`, `12h`, or `false` to disable. |

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
  https://music.youtube.com/channel/UCkkHg-BBHwyw
  ```
  adding a new link by docker command:
  ```plaintext
  docker exec cruix-music-archiver bash -c 'echo "# ARTIST NAME" >> ./artists.txt'
  docker exec cruix-music-archiver bash -c 'echo "https://music.youtube.com/channel/UCHg-BBwyw" >> ./artists.txt'
  ```

- **genres_cache.txt**  
  this cache is built through an api and applied to the artist's musical style. If you do not agree with the information provided by the api, send me a message 😊


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


## 📄:  USER AGREEMENT AND DONATIONS

This project was developed exclusively for **educational purposes and personal use**, and aims to assist users in organizing and managing their music libraries. The software uses `yt-dlp`, an open-source tool, to download content only from publicly accessible sources. It is strictly prohibited to use the software to download, distribute, or share any content protected by copyright without explicit authorization from the copyright holder.

***Important Notice:*** The software does not host, store, or distribute any media files. It does not provide direct access to any content. All downloads are initiated, managed, and controlled entirely by the user. The user is solely responsible for ensuring that the use of the software complies with all applicable copyright laws, the terms of service of the websites from which content is downloaded, and relevant local regulations. It is the user's responsibility to ensure that the downloaded content is legally available for download and distribution and that they have the proper permissions. Any unauthorized download or distribution of copyrighted content is illegal, and the user assumes full legal responsibility for such actions.

***Legal Compliance:*** By using this software, the user agrees to comply with all applicable copyright laws, the terms of service of any websites from which content is downloaded, and relevant local regulations. The developers assume no responsibility for actions taken by users that violate copyright laws or terms of service. The responsibility for legal compliance lies entirely with the user. The user must ensure that the downloaded content is legally available for download and distribution.

***Prohibition of Illegal Use:*** This software is not intended for, and must not be used for, any illegal activity. This includes, but is not limited to, downloading, distributing, or sharing copyrighted content without proper authorization. The user must not use the software to circumvent any digital rights management (DRM) or other similar protections.

***Legal Disclaimer:*** The developers do not endorse, facilitate, or support the illegal use of this software. By using the software, the user acknowledges that they are fully responsible for their actions and commit to complying with current legislation. The developers will not be responsible for any legal actions resulting from the misuse of the software.

***Donations and Sponsor:*** Donations are voluntary and do not provide any special access to content, nor do they allow bypassing legal restrictions or altering the functionality of the software in any way. Donations do not affect the user's ability to use the software and are in no way related to any access to illegal content.

---

for more `yt-dlp` options, check the [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp#usage-and-options).