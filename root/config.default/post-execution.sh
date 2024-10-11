#!/usr/bin/with-contenv bash

# identifies the output directory from the '--output' argument
output_dir="/downloads"

# remove cache files in the output directory and process post-processing scripts
if [ -d "$output_dir" ]; then

  echo -e "\ncleaning cache files in directory: $output_dir"

  find "$output_dir" -type d -empty -delete

  # post-processing scripts

  echo -e "executing post-processing scripts for the music library update"

  sleep '3'

  python3 /app/extended-scripts/logs_cleaner.py

  sleep '3'

  python3 /app/extended-scripts/wordnet_corpus_downloader.py

  sleep '3'

  python3 /app/extended-scripts/invalid_characters_remover.py

  sleep '3'
  umask "$UMASK"
  /app/extended-scripts/complete_missing_covers.sh

  sleep '3'

  python3 /app/extended-scripts/trash_collector.py

  sleep '3'

  find "$output_dir" -type d -empty -delete

  sleep '3'

  python3 /app/extended-scripts/unofficial_albums_mover.py

  sleep '3'

  find "$output_dir" -type d -empty -delete

  sleep '3'
  umask "$UMASK"
  /app/extended-scripts/loudnorm.sh

  sleep '3'

  python3 /app/extended-scripts/capitalize_tags_files_and_folders.py

  sleep '3'

  python3 /app/extended-scripts/capitalize_folders_and_tags_accents.py

  sleep '3'

  python3 /app/extended-scripts/tags_and_folders_strings_fixer.py

  sleep '3'

  python3 /app/extended-scripts/release_year_update.py

  sleep '3'

  python3 /app/extended-scripts/deezer_db_downloader.py

  sleep '3'

  python3 /app/extended-scripts/lastgenre.py

  sleep '3'

  python3 /app/extended-scripts/capitalize_fixer.py

  sleep '3'

  python3 /app/extended-scripts/genre_fixer.py

  sleep '3'

  python3 /app/extended-scripts/trash_collector.py

  sleep '3'

  find "$output_dir" -type d -empty -delete

  sleep '3'
  umask "$UMASK"
  /app/extended-scripts/complete_missing_covers.sh

  sleep '3'

  python3 /app/extended-scripts/missing_covers_downloader.py

  sleep '3'
  umask "$UMASK"
  /app/extended-scripts/complete_missing_covers.sh

  sleep '3'

  python3 /app/extended-scripts/trash_collector.py

  sleep '3'

  find "$output_dir" -type d -empty -delete

  sleep '3'

  python3 /app/extended-scripts/jellyfin_album_downloader.py

  sleep '3'

  python3 /app/extended-scripts/jellyfin_artist_downloader.py

  sleep '3'

  python3 /app/extended-scripts/add_mp3_thumbnail.py

else
  echo -e "\noutput directory not found: $output_dir"
fi