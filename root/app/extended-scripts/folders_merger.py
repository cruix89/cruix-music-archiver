import os
import logging
import shutil


def setup_directories():
    try:
        music_directory = '/music'
        logs_directory = '/config/logs'
        duplicate_folders_directory = '/config/duplicate-folders'
        return music_directory, logs_directory, duplicate_folders_directory
    except Exception as error:
        logging.error(f'error setting up directories: {error}')
        raise


def process_artists_top_level(base_directory, duplicate_folders_directory):
    try:
        logging.info("processing artist directories at the top level...")

        # dictionary to map artist base names to their paths
        artist_map = {}

        # iterate only the top-level directories
        for folder_name in os.listdir(base_directory):
            artist_path = os.path.join(base_directory, folder_name)

            # ensure it's a directory
            if not os.path.isdir(artist_path):
                continue

            # extract base name (e.g., `elana_dara` from `elana_dara_copy1`)
            base_name = folder_name.split('_copy')[0]

            # group directories by base name
            artist_map.setdefault(base_name, []).append(artist_path)

        # process duplicates for each artist base name
        for base_name, artist_group in artist_map.items():
            if len(artist_group) > 1:
                logging.info(f"found duplicate artist directories for '{base_name}': {artist_group}")

                # move duplicate artist directories to /config/duplicate-folders
                for duplicate_path in artist_group[1:]:
                    target_folder = os.path.join(duplicate_folders_directory, os.path.basename(duplicate_path))
                    logging.info(f"moving duplicate artist directory: {duplicate_path} -> {target_folder}")
                    shutil.move(duplicate_path, target_folder)

        logging.info("artist directory processing completed successfully.")
    except Exception as error:
        logging.error(f"error processing artist directories: {error}")
        raise


# CONFIGURE LOGGING
try:
    music_dir, logs_dir, duplicate_dir = setup_directories()
    log_path = os.path.join(logs_dir, 'artist_folders_merger.log')
    logging.basicConfig(filename=log_path, level=logging.INFO)
except Exception as e:
    print(f'[cruix-music-archiver] error setting up logging: {e}')
    raise

# NOTIFY START OF PROCESS
print("[cruix-music-archiver] starting the artist folder merging process... 🎶  💥  let the transformation begin!")

# PROCESS MUSIC DIRECTORY
try:
    process_artists_top_level(music_dir, duplicate_dir)  # process artist folders at the top level
except Exception as e:
    logging.error(f'error executing script: {e}')
    raise

# NOTIFY END OF PROCESS
print("[cruix-music-archiver] artist folder processing completed successfully... 🎉  your files are now perfectly organized and ready to shine!")