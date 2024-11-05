#!/usr/bin/with-contenv bash

# directory's config
downloads_dir="/downloads"
music_dir="/music"
cache_dir="/config/cache"
logs_dir="/config/logs"
recycle_bin_dir="/config/recycle-bin"
unofficial_albums_dir="/config/unofficial-albums"

# remove cache files in the output directory and process post-processing scripts
if [ -d "$downloads_dir" ]; then

  echo -e "\ncleaning cache files in directory's: /cache /logs /downloads"

  sleep '5'
  mkdir -p $cache_dir
  find $cache_dir -type f -delete
  find $cache_dir -type d -empty -mindepth 1 -delete

  sleep '5'
  find "$downloads_dir" -mindepth 1 -type d -empty -delete

  echo -e "executing post-processing scripts for the music library update"

  # post-processing scripts in downloads folder

  sleep '5'
  mkdir -p $logs_dir
  find $logs_dir -type f -delete

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

  sleep '5'
  python3 /app/extended-scripts/capitalize_tags_files_and_folders.py

  sleep '5'
  python3 /app/extended-scripts/capitalize_folders_and_tags_accents.py

  sleep '5'
  python3 /app/extended-scripts/tags_and_folders_strings_fixer.py

  sleep '5'
  python3 /app/extended-scripts/release_year_update.py

  sleep '5'
  python3 /app/extended-scripts/deezer_db_downloader.py

  sleep '5'
  python3 /app/extended-scripts/lastgenre.py

  sleep '5'
  python3 /app/extended-scripts/capitalize_fixer.py

  sleep '5'
  python3 /app/extended-scripts/genre_fixer.py

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
  python3 /app/extended-scripts/jellyfin_album_downloader.py

  sleep '5'
  python3 /app/extended-scripts/jellyfin_artist_downloader.py

  sleep '5'
  python3 /app/extended-scripts/poweramp_album_downloader.py

  sleep '5'
  python3 /app/extended-scripts/poweramp_artist_downloader.py

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
  python3 /app/extended-scripts/trash_collector.py

  sleep '5'
  find "$music_dir" -mindepth 1 -type d -empty -delete

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

  echo -e "\ncleaning old files in recycle-bin and unofficial-albums\n"

  mkdir -p $recycle_bin_dir
  mkdir -p $unofficial_albums_dir
  find $recycle_bin_dir -depth -mtime +6 -exec rm -rf {} \;
  find $unofficial_albums_dir -depth -mtime +6 -exec rm -rf {} \;

  echo -e "old files in recycle-bin and unofficial-albums successfully cleaned.\n"

else
  echo -e "output directory not found: $downloads_dir"
fi