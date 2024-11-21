#!/usr/bin/with-contenv bash

# directory's config
downloads_dir="/downloads"
music_dir="/music"
cache_dir="/config/cache"
logs_dir="/config/logs"
recycle_bin_dir="/config/recycle-bin"
unofficial_albums_dir="/config/unofficial-albums"
dz_db_dir="/config/dz-db"

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

  # scripts running only in mp3 files

  sleep '5'
  python3 /app/extended-scripts/capitalize_tags_files_and_folders.py

  sleep '5'
  python3 /app/extended-scripts/tags_and_folders_strings_fixer.py

  sleep '5'
  python3 /app/extended-scripts/artists_folders_merger.py

  sleep '5'
  python3 /app/extended-scripts/capitalize_folders_and_tags_accents.py

  sleep '5'
  python3 /app/extended-scripts/tags_and_folders_strings_fixer.py

  sleep '5'
  python3 /app/extended-scripts/release_year_update.py

  sleep '5'
  python3 /app/extended-scripts/dz_db_downloader.py

  sleep '5'
  python3 /app/extended-scripts/lastgenre.py

  sleep '5'
  python3 /app/extended-scripts/capitalize_fixer.py

  # sleep '5'
  # python3 /app/extended-scripts/genre_fixer.py

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

  sleep '5'
  python3 /app/extended-scripts/artists_invalid_characters_remover.py

  sleep '5'
  python3 /app/extended-scripts/artists_tag_fixer.py

  sleep '5'
  python3 /app/extended-scripts/add_mp3_thumbnail.py

  sleep '5'
  python3 /app/extended-scripts/artists_folder_capitalize.py

  sleep '5'
  python3 /app/extended-scripts/artists_folder_fixer.py

  sleep '5'
  python3 /app/extended-scripts/unofficial_albums_mover.py

  sleep '5'
  find "$music_dir" -mindepth 1 -type d -empty -delete

  sleep '5'
  python3 /app/extended-scripts/artist_disambiguator.py

  sleep '5'
  find "$music_dir" -mindepth 1 -type d -empty -delete

  sleep '5'
  python3 /app/extended-scripts/dz_db_downloader.py

  sleep '5'
  python3 /app/extended-scripts/untitled_album_folder.py

  sleep '5'
  python3 /app/extended-scripts/untitled_album_tag.py

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

  sleep '5'
  python3 /app/extended-scripts/tracks_updater.py

  sleep '5'
  python3 /app/extended-scripts/untitled_album_cover.py

  echo -e "[cruix-music-archiver] cleaning up the digital cobwebs in /recycle-bin, /dz-db, and /unofficial-albums. out with the old, in with the tidy!"

  mkdir -p $recycle_bin_dir
  mkdir -p $unofficial_albums_dir
  mkdir -p $dz_db_dir
  find $recycle_bin_dir -depth -mtime +6 -exec rm -rf {} \;
  find $unofficial_albums_dir -depth -mtime +6 -exec rm -rf {} \;
  find $dz_db_dir -depth -mtime +6 -exec rm -rf {} \;

  echo -e "[cruix-music-archiver] mission accomplished! old files in /recycle-bin, /dz-db, and /unofficial-albums have been successfully swept away.  🗑️  ✨"

else
  echo -e "[cruix-music-archiver] ⚠️  oops! output directory not found: $downloads_dir. did it get lost in the void? 🌌"
fi