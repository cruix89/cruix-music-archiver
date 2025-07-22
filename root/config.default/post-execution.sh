#!/usr/bin/with-contenv bash

# directory's config
downloads_dir="/downloads"
music_dir="/music"
cache_dir="/config/cache"
logs_dir="/config/logs"
recycle_bin_dir="/config/recycle-bin"
unofficial_albums_dir="/config/unofficial-albums"
dz_db_dir="/config/dz-db"
merged_folders_backup_dir="/config/merged-folders-backup"

mkdir -p $downloads_dir
mkdir -p $music_dir
mkdir -p $cache_dir
mkdir -p $logs_dir
mkdir -p $recycle_bin_dir
mkdir -p $unofficial_albums_dir
mkdir -p $dz_db_dir
mkdir -p $merged_folders_backup_dir

# remove cache files in the output directory and process post-processing scripts
if [ -d "$downloads_dir" ]; then

  echo -e "[cruix-music-archiver] Initiating Cleanup Protocol... Purging Cache Files From the Following Directories: /cache and /logs 🧹  ✨"

  sleep '5'
  mkdir -p $cache_dir
  find $cache_dir -type f -delete
  find $cache_dir -type d -empty -mindepth 1 -delete

  sleep '5'
  mkdir -p $logs_dir
  find $logs_dir -type f -delete

  echo -e "[cruix-music-archiver] Running the [cruix-music-archiver] Scripts... Preparing to Update the Music Library With the Precision of a Time-Traveling DJ! 🕰️  🎶"

  # post-processing scripts in downloads folder

  sleep '5'
  python3 /app/scripts/downloads_invalid_characters_remover.py

  sleep '5'
  python3 /app/scripts/downloads_mover.py

  # post-processing scripts in music folder

  sleep '5'
  python3 /app/scripts/music_invalid_characters_remover.py

  sleep '5'
  umask "$UMASK"
  /app/scripts/complete_missing_covers.sh

  sleep '5'
  python3 /app/scripts/trash_collector.py

  sleep '5'
  find "$music_dir" -mindepth 1 -type d -empty -delete

  sleep '5'
  umask "$UMASK"
  /app/scripts/loudnorm.sh

  # the processes below are only executed in the mp3 extension

  # folder merger correction 1

  sleep '5'
  python3 /app/scripts/capitalize_tags_files_and_folders.py

  sleep '5'
  python3 /app/scripts/artists_folders_fixer.py

  sleep '5'
  python3 /app/scripts/youtube_tracks_folder.py

  sleep '5'
  python3 /app/scripts/youtube_tracks_tag.py

  sleep '5'
  python3 /app/scripts/artists_folders_merger.py

  # folder merger correction 2

  sleep '5'
  python3 /app/scripts/capitalize_tags_files_and_folders.py

  sleep '5'
  python3 /app/scripts/artists_folders_fixer.py

  sleep '5'
  python3 /app/scripts/youtube_tracks_folder.py

  sleep '5'
  python3 /app/scripts/youtube_tracks_tag.py

  sleep '5'
  python3 /app/scripts/artists_folders_merger.py

  # folder merger correction 3

  sleep '5'
  python3 /app/scripts/capitalize_tags_files_and_folders.py

  sleep '5'
  python3 /app/scripts/artists_folders_fixer.py

  sleep '5'
  python3 /app/scripts/youtube_tracks_folder.py

  sleep '5'
  python3 /app/scripts/youtube_tracks_tag.py

  sleep '5'
  python3 /app/scripts/artists_folders_merger.py

  # folder merger correction 4

  sleep '5'
  python3 /app/scripts/capitalize_tags_files_and_folders.py

  sleep '5'
  python3 /app/scripts/artists_folders_fixer.py

  sleep '5'
  python3 /app/scripts/youtube_tracks_folder.py

  sleep '5'
  python3 /app/scripts/youtube_tracks_tag.py

  sleep '5'
  python3 /app/scripts/artists_folders_merger.py

  # folder merger correction 5

  sleep '5'
  python3 /app/scripts/capitalize_tags_files_and_folders.py

  sleep '5'
  python3 /app/scripts/artists_folders_fixer.py

  sleep '5'
  python3 /app/scripts/youtube_tracks_folder.py

  sleep '5'
  python3 /app/scripts/youtube_tracks_tag.py

  sleep '5'
  python3 /app/scripts/artists_folders_merger.py

  # capitalize accents do lowercase

  sleep '5'
  python3 /app/scripts/capitalize_folders_and_tags_accents.py

  # fixer strings based in fixer.txt

  sleep '5'
  python3 /app/scripts/tags_and_folders_strings_fixer.py

  # fixer year tag do yyyy

  sleep '5'
  python3 /app/scripts/release_year_update.py

  # db download

  sleep '5'
  python3 /app/scripts/dz_db_downloader.py

  # db cleaner

  sleep '5'
  find $dz_db_dir -type d -empty -mindepth 1 -delete

  # genre api

  sleep '5'
  python3 /app/scripts/lastgenre.py

  # capitalize

  sleep '5'
  python3 /app/scripts/capitalize_fixer.py

  sleep '5'
  python3 /app/scripts/tags_and_folders_strings_fixer.py

  # covers configuration

  sleep '5'
  umask "$UMASK"
  /app/scripts/complete_missing_covers.sh

  sleep '5'
  python3 /app/scripts/trash_collector.py

  sleep '5'
  find "$music_dir" -mindepth 1 -type d -empty -delete

  sleep '5'
  python3 /app/scripts/missing_covers_downloader.py

  sleep '5'
  umask "$UMASK"
  /app/scripts/complete_missing_covers.sh

  sleep '5'
  python3 /app/scripts/trash_collector.py

  sleep '5'
  find "$music_dir" -mindepth 1 -type d -empty -delete

  # remove invalid characters from artists

  sleep '5'
  python3 /app/scripts/artists_invalid_characters_remover.py

  # fixer artists tag (multiple artists)

  sleep '5'
  python3 /app/scripts/artists_tag_fixer.py

  # add mp3 thumbs

  sleep '5'
  python3 /app/scripts/add_mp3_thumbnail.py

  # tracks fixer api

  sleep '5'
  python3 /app/scripts/album_updater.py

  sleep '5'
  python3 /app/scripts/track_name_updater.py

  sleep '5'
  python3 /app/scripts/track_number_updater.py

  # capitalization artists folders to uppercase

  sleep '5'
  python3 /app/scripts/artists_folder_capitalize.py

  sleep '5'
  python3 /app/scripts/artists_folders_fixer.py

  # disambiguation process

  sleep '5'
  python3 /app/scripts/artist_disambiguator.py

  sleep '5'
  python3 /app/scripts/trash_collector.py

  sleep '5'
  find "$music_dir" -mindepth 1 -type d -empty -delete

  # move unofficial albums

  sleep '5'
  python3 /app/scripts/unofficial_albums_mover.py

  sleep '5'
  find "$music_dir" -mindepth 1 -type d -empty -delete

  # media centers covers configuration

  sleep '5'
  python3 /app/scripts/dz_db_downloader.py

  sleep '5'
  find $dz_db_dir -type d -empty -mindepth 1 -delete

  sleep '5'
  python3 /app/scripts/jellyfin_album_downloader.py

  sleep '5'
  python3 /app/scripts/jellyfin_artist_downloader.py

  sleep '5'
  python3 /app/scripts/plex_album_downloader.py

  sleep '5'
  python3 /app/scripts/plex_artist_downloader.py

  sleep '5'
  python3 /app/scripts/unknown_artist_cover.py

  mkdir -p $recycle_bin_dir
  mkdir -p $unofficial_albums_dir
  mkdir -p $dz_db_dir
  mkdir -p $merged_folders_backup_dir
  find $recycle_bin_dir -depth -mtime +6 -exec rm -rf {} \;
  find $unofficial_albums_dir -depth -mtime +6 -exec rm -rf {} \;
  find $dz_db_dir -depth -mtime +6 -exec rm -rf {} \;

  echo -e "[cruix-music-archiver] Mission Accomplished! Old Files in /recycle-bin, /dz-db and /unofficial-albums Have Been Successfully Swept Away! 🗑️  ✨"

else
  echo -e "[cruix-music-archiver] ⚠️  Oops! Output Directory Not Found: $downloads_dir. Did It Get Lost in the Void? 🌌"
fi