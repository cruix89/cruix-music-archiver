import os
import logging
import shutil


def setup_directories():
    try:
        music_directory = '/music'
        logs_directory = '/config/logs'
        duplicate_folders_directory = '/config/duplicate-folders'
        cache_directory = '/config/cache'
        return music_directory, logs_directory, duplicate_folders_directory, cache_directory
    except Exception as error:
        logging.error(f'error setting up directories: {error}')
        raise


def process_artists_top_level(base_directory, duplicate_folders_directory, cache_directory):
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

        # process each group in the artist map
        for base_name, artist_group in artist_map.items():
            # create a directory in /config/cache for the base name
            cache_folder = os.path.join(cache_directory, base_name)
            os.makedirs(cache_folder, exist_ok=True)

            # copy content of all grouped folders to the cache directory
            for folder in artist_group:
                for item in os.listdir(folder):
                    source_path = os.path.join(folder, item)
                    target_path = os.path.join(cache_folder, item)

                    if os.path.isdir(source_path):
                        logging.info(f"copying directory: {source_path} -> {target_path}")
                        shutil.copytree(source_path, target_path, dirs_exist_ok=True)
                    else:
                        logging.info(f"copying file: {source_path} -> {target_path}")
                        shutil.copy2(source_path, target_path)

            # move original folders to the duplicate folder directory
            for folder in artist_group:
                target_folder = os.path.join(duplicate_folders_directory, os.path.basename(folder))
                logging.info(f"moving original folder: {folder} -> {target_folder}")
                shutil.move(folder, target_folder)

            # move the merged cache folder back to the original directory
            target_path = os.path.join(base_directory, base_name)
            logging.info(f"moving merged directory: {cache_folder} -> {target_path}")
            shutil.move(cache_folder, target_path)

        logging.info("artist directory processing completed successfully.")
    except Exception as error:
        logging.error(f"error processing artist directories: {error}")
        raise


# CONFIGURE LOGGING
try:
    music_dir, logs_dir, duplicate_dir, cache_dir = setup_directories()
    log_path = os.path.join(logs_dir, 'artist_folders_merger.log')
    os.makedirs(logs_dir, exist_ok=True)  # ensure the logs directory exists
    logging.basicConfig(filename=log_path, level=logging.INFO)
except Exception as e:
    print(f'[cruix-music-archiver] error setting up logging: {e}')
    raise

# NOTIFY START OF PROCESS
print("[cruix-music-archiver] starting the artist folder merging process... 🎶  💥  let the transformation begin!")

# PROCESS MUSIC DIRECTORY
try:
    process_artists_top_level(music_dir, duplicate_dir, cache_dir)  # process artist folders at the top level
except Exception as e:
    logging.error(f'error executing script: {e}')
    raise

# NOTIFY END OF PROCESS
print("[cruix-music-archiver] artist folder processing completed successfully... 🎉  your files are now perfectly organized and ready to shine!")