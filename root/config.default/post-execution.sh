#!/usr/bin/with-contenv bash

# directory's config
downloads_dir="/downloads"
music_dir="/music"
cache_dir="/config/cache"
logs_dir="/config/logs"
recycle_bin_dir="/config/recycle-bin"
unofficial_albums_dir="/config/unofficial-albums"
dz_db_dir="/config/dz-db"
duplicate_artist_dir="/config/duplicate-artists-folders"

mkdir -p $downloads_dir
mkdir -p $music_dir
mkdir -p $cache_dir
mkdir -p $logs_dir
mkdir -p $recycle_bin_dir
mkdir -p $unofficial_albums_dir
mkdir -p $dz_db_dir
mkdir -p $duplicate_artist_dir

# remove cache files in the output directory and process post-processing scripts
if [ -d "$downloads_dir" ]; then

  echo -e "[cruix-music-archiver] initiating cleanup protocol... purging cache files from the following directories: /cache, /logs, and /downloads. 🧹  ✨"

  sleep '5'
  mkdir -p $cache_dir
  find $cache_dir -type f -delete
  find $cache_dir -type d -empty -mindepth 1 -delete

  sleep '5'
  find "$downloads_dir" -mindepth 1 -type d -empty -delete

  sleep '5'
  mkdir -p $logs_dir
  find $logs_dir -type f -delete

  echo -e "[cruix-music-archiver] running the cruix-music-archiver scripts... preparing to update the music library with the precision of a time-traveling DJ! 🕰️  🎶"

  # post-processing scripts in downloads folder

  sleep '5'
  python3 /app/extended-scripts/downloads_invalid_characters_remover.py

  sleep '5'
  python3 /app/extended-scripts/downloads_mover.py

  # post-processing scripts in music folder

  sleep '5'
  python3 /app/extended-scripts/music_invalid_characters_remover.py

  sleep '5'
  umask "$UMASK"
  /app/extended-scripts/complete_missing_covers.sh

  sleep '5'
  python3 /app/extended-scripts/trash_collector.py

  sleep '5'
  find "$music_dir" -mindepth 1 -type d -empty -delete

  sleep '5'
  umask "$UMASK"
  /app/extended-scripts/loudnorm.sh

  # the processes below are only executed in the mp3 extension

  # folder merger correction

  sleep '5'
  python3 /app/extended-scripts/capitalize_tags_files_and_folders.py

  sleep '5'
  python3 /app/extended-scripts/artists_folders_fixer.py

  sleep '5'
  python3 /app/extended-scripts/untitled_album_folder.py

  sleep '5'
  python3 /app/extended-scripts/untitled_album_tag.py

  sleep '5'
  python3 /app/extended-scripts/artists_folders_merger.py

  # capitalize accents do lowercase

  sleep '5'
  python3 /app/extended-scripts/capitalize_folders_and_tags_accents.py

  # fixer strings based in fixer.txt

  sleep '5'
  python3 /app/extended-scripts/tags_and_folders_strings_fixer.py

  # fixer year tag do yyyy

  sleep '5'
  python3 /app/extended-scripts/release_year_update.py

  # db download

  sleep '5'
  python3 /app/extended-scripts/dz_db_downloader.py

  # genre api

  sleep '5'
  python3 /app/extended-scripts/lastgenre.py

  # capitalize

  sleep '5'
  python3 /app/extended-scripts/capitalize_fixer.py

  # sleep '5'
  # python3 /app/extended-scripts/genre_fixer.py

  # covers configuration

  sleep '5'
  umask "$UMASK"
  /app/extended-scripts/complete_missing_covers.sh

  sleep '5'
  python3 /app/extended-scripts/missing_covers_downloader.py

  sleep '5'
  umask "$UMASK"
  /app/extended-scripts/complete_missing_covers.sh

  sleep '5'
  python3 /app/extended-scripts/trash_collector.py

  sleep '5'
  find "$music_dir" -mindepth 1 -type d -empty -delete

  # remove characters from artists

  sleep '5'
  python3 /app/extended-scripts/artists_invalid_characters_remover.py

  # fixer artists tag (multiple artists)

  sleep '5'
  python3 /app/extended-scripts/artists_tag_fixer.py

  # add mp3 thumbs

  sleep '5'
  python3 /app/extended-scripts/add_mp3_thumbnail.py

  # move unofficial albums

  sleep '5'
  python3 /app/extended-scripts/unofficial_albums_mover.py

  sleep '5'
  find "$music_dir" -mindepth 1 -type d -empty -delete

  # disambiguator process

  sleep '5'
  python3 /app/extended-scripts/artist_disambiguator.py

  sleep '5'
  find "$music_dir" -mindepth 1 -type d -empty -delete

  # media centers covers configuration

  sleep '5'
  python3 /app/extended-scripts/dz_db_downloader.py

  sleep '5'
  python3 /app/extended-scripts/jellyfin_album_downloader.py

  sleep '5'
  python3 /app/extended-scripts/jellyfin_artist_downloader.py

  sleep '5'
  python3 /app/extended-scripts/plex_album_downloader.py

  sleep '5'
  python3 /app/extended-scripts/plex_artist_downloader.py

  sleep '5'
  python3 /app/extended-scripts/various_artists_cover.py

  # tracks fixer api

  sleep '5'
  python3 /app/extended-scripts/tracks_updater.py

  # untitled album cover fixer

  sleep '5'
  python3 /app/extended-scripts/untitled_album_cover.py

  # capitalization artists folders to uppercase

  sleep '5'
  python3 /app/extended-scripts/artists_folder_capitalize.py

  echo -e "[cruix-music-archiver] cleaning up the digital cobwebs in /recycle-bin, /dz-db, /duplicate-artists-folders and /unofficial-albums. out with the old, in with the tidy!   🗑️  ✨"

  mkdir -p $recycle_bin_dir
  mkdir -p $unofficial_albums_dir
  mkdir -p $dz_db_dir
  mkdir -p $duplicate_artist_dir
  find $recycle_bin_dir -depth -mtime +6 -exec rm -rf {} \;
  find $unofficial_albums_dir -depth -mtime +6 -exec rm -rf {} \;
  find $dz_db_dir -depth -mtime +6 -exec rm -rf {} \;
  find $duplicate_artist_dir -depth -mtime +6 -exec rm -rf {} \;

  echo -e "[cruix-music-archiver] mission accomplished! old files in /recycle-bin, /dz-db, /duplicate-artists-folders and /unofficial-albums have been successfully swept away.  🗑️  ✨"

else
  echo -e "[cruix-music-archiver] ⚠️  oops! output directory not found: $downloads_dir. did it get lost in the void? 🌌"
fi