# cruix89 / cruix-music-archiver
[![GitHub last commit](https://img.shields.io/github/last-commit/cruix89/cruix-music-archiver?logo=github)](https://github.com/cruix89/cruix-music-archiver/actions/workflows/push-unstable-image.yml/)
[![GitHub Automated build](https://img.shields.io/github/actions/workflow/status/cruix89/cruix-music-archiver/push-release-version-image.yml?logo=github)](https://github.com/cruix89/cruix-music-archiver/actions/workflows/push-release-version-image.yml/)
[![Image Size](https://img.shields.io/docker/image-size/cruix89/cruix-music-archiver/latest?style=flat&logo=docker)](https://hub.docker.com/r/cruix89/cruix-music-archiver/)
[![Docker Pulls](https://img.shields.io/docker/pulls/cruix89/cruix-music-archiver?style=flat&logo=docker)](https://hub.docker.com/r/cruix89/cruix-music-archiver/)
[![Docker Stars](https://img.shields.io/docker/stars/cruix89/cruix-music-archiver?style=flat&logo=docker)](https://hub.docker.com/r/cruix89/cruix-music-archiver/)

**automated yt-dlp docker image for downloading YouTube Music discography's/playlists/single tracks or music of others platforms supported by youtube-dlp**

Docker Hub page [here](https://hub.docker.com/r/cruix89/cruix-music-archiver).  
yt-dlp documentation [here](https://github.com/yt-dlp/yt-dlp).

# Features
* **Easy Usage with Minimal Setup**
    * Quality options with env parameter
    * Included format selection argument
    * Included set of starter arguments
* **Automatic Updates**
    * Self updating container
    * Automated image building
* **Automatic Downloads**
    * Interval options with env parameter
    * Channel URLs from file
* **PUID/PGID**
* **yt-dlp Options**
   * SponsorBlock
   * Format
   * Quality
   * Download archive
   * Output
   * Thumbnails
   * Geo bypass
   * Proxy support
   * Metadata
   * Etc

# Quick Start

"download music from my artists.txt url file:"
<br>

```
docker run -d \
    --name cruix-music-archiver \
    -v youtube-dl_data:/config \
    -v <PATH>:/downloads \
    cruix89/cruix-music-archiver
```
**Explanation**
* `-v youtube-dl_data:/config`  
  This makes a Docker volume where your config files are saved, named: `youtube-dl_data`.

* `-v <PATH>:/downloads`  
  This makes a bind mount where the music are downloaded.  
  This is where on your Docker host you want youtube-dl to download music.  
  Replace `<PATH>`, example: `-v /media/youtube-dl:/downloads`

# Env Parameters
`-e <Parameter>=<Value>`

|         Parameter         |        Value (Default)         | What it does                                                                                                                                                                                                                                                                                                                                           |
|:-------------------------:|:------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|           `TZ`            |        `Europe/London`         | Specify TimeZone for the log timestamps to be correct.                                                                                                                                                                                                                                                                                                 |
|          `PUID`           |            (`911`)             | If you need to specify UserID for file permission reasons.                                                                                                                                                                                                                                                                                             |
|          `PGID`           |            (`911`)             | If you need to specify GroupID for file permission reasons.                                                                                                                                                                                                                                                                                            |
|          `UMASK`          |            (`022`)             | If you need to specify umask for file permission reasons.                                                                                                                                                                                                                                                                                              |
|     `youtubedl_debug`     |        `true` (`false`)        | Used to enable verbose mode.                                                                                                                                                                                                                                                                                                                           |
|   `youtubedl_lockfile`    |        `true` (`false`)        | Used to enable youtubedl-running, youtubedl-completed files in downloads directory. Useful for external scripts.                                                                                                                                                                                                                                       |
|   `youtubedl_interval`    | `1h` (`3h`) `12h` `3d` `false` | If you want to change the default download interval.<br>This can be any value compatible with [gnu sleep](https://github.com/tldr-pages/tldr/blob/main/pages/linux/sleep.md) or if set to false, the container will shutoff after executing. A low interval value risks you being ip-banned by YouTube.<br>1 hour, (3 hours), 12 hours, 3 days, false. |

# Image Tags
* **`unstable`**
    * Automatically built when a new GitHub commit is pushed.
    * Container updates to the newest yt-dlp commit while running.
* **`latest`**
    * Automatically built when a new version of yt-dlp is released.
    * Container updates to the latest version of yt-dlp while running.
* **`v<VERSION>`**
    * Automatically built when a new version of yt-dlp is released.
    * Does not update.

# Configure cruix-music-archiver

* **artists.txt**

    File location: `/config/artists.txt`.  
    This is where you input all the YouTube Music artists/playlists links (or any valid URL) you want to have music downloaded from.
    ```
    # One per line
    # Example:
    https://music.youtube.com/channel/UC2DXTFA6ACS0Qb9QtFlAVDg
    ```
    You can also specify additional args to be used per URL. This is done by adding args after the URL separated by the ` | ` character.  
    These will override any conflicting args from `args.conf`.
    ```
    # Examples
    # Output to 'named' folder instead of channel name
    https://music.youtube.com/channel/UC2DXTFA6ACS0Qb9QtFlAVDg | --output '/downloads/named/%(title)s.%(ext)s'

    # Use regex to only download music matching words
    https://music.youtube.com/channel/UC2DXTFA6ACS0Qb9QtFlAVDg | --no-match-filter --match-filter '!is_live & title~=(?i)words.*to.*match'

    # Use regex to only download music not matching words
    https://music.youtube.com/channel/UC2DXTFA6ACS0Qb9QtFlAVDg | --no-match-filter --match-filter '!is_live & title!~=(?i)words.*to.*exclude'

    # Download a whole playlist, also disable reverse download order
    https://music.youtube.com/playlist?list=D9sLB5EVaCarZ7lbpQfGch3jJuYCRt | --playlist-end '-1' --no-playlist-reverse
    ```
    Adding with Docker:  
    `docker exec youtube-dl bash -c 'echo "# NAME" >> ./artists.txt'`  
    `docker exec youtube-dl bash -c 'echo "URL" >> ./artists.txt'`

    It is recommended to use the UCID-based URLs, they look like: `music.youtube.com/channel/UC2DXTFA6ACS0Qb9QtFlAVDg`, as the other ones might get changed.
    You find the UCID-based URL by going to a music and copy from bar.

* **pre-execution.sh**

    File location: `/config/pre-execution.sh`.  
    This is an optional user defined script that is executed before youtube-dl starts downloading musics.

* **post-execution.sh**

    File location: `/config/post-execution.sh`.  
    This is an optional user defined script that is executed after youtube-dl has finished its full execution.

* **archive.txt**

    File location: `/config/archive.txt`.&nbsp;&nbsp;&nbsp;*delete to make youtube-dl forget downloaded musics*  
    This is where youtube-dl stores all previously downloaded musics IDs.

* **args.conf**

    File location: `/config/args.conf`.&nbsp;&nbsp;&nbsp;*delete and restart container to restore default arguments. 
    This is where all youtube-dl execution arguments are, you can add or remove them however you like. If unmodified this file is automatically updated.

    **Unsupported arguments**
    * `--config-location`, hardcoded to `/config/args.conf`.
    * `--batch-file`, hardcoded to `/config/artists.txt`.

    **Default arguments**
    * `--output "/downloads/%(channel)s/%(album)s/%(title)s.%(ext)s"`, makes youtube-dl create separate folders for each artist and use the music title for the filename.
    * `--parse-metadata "channel:%(album_artist)s" --add-metadata`, add artist album ID3 tag using the artist channel name.
    * `--format bestaudio`, make youtube-dlp download the best audio possible.
    * `--force-overwrites`, make youtube-dlp overwrites the files if a previous download was failed. 
    * `--windows-filenames`, prevent youtube-dlp to grab filenames incompatible with windows filesystem.
    * `--trim-filenames 260`, prevent youtube-dlp to grab filenames too long.
    * `--newline`, add a new line each percent of download conclusion.
    * `--progress`, log each percent in download progress.
    * `--write-all-thumbnails`, makes youtube-dlp download music thumbnails.
    * `--extract-audio`, makes youtube-dlp create the audio file.
    * `--audio-format flac`, download the audio file to Free Lossless Audio Codec format. 
    * `--embed-metadata`, makes youtube-dl grab ID3 tags in the music file.
    * `--sleep-requests 1.5`, make youtube-dlp to wait 5 second for every request to prevent block access. (audio files are downloaded very quickly, causing many requests)

    yt-dlp configuration options documentation [here](https://github.com/yt-dlp/yt-dlp#usage-and-options).