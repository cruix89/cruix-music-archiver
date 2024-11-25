import os
import logging
import shutil
from pathlib import Path


def setup_directories():
    """
    setup directories and ensure they exist
    """
    try:
        music_directory = Path('/music').resolve()  # Usando Path para garantir o tipo correto
        logs_directory = Path('/config/logs').resolve()
        duplicate_folders_directory = Path('/config/duplicate-artists-folders').resolve()
        cache_directory = Path('/config/cache').resolve()

        # Ensure directories exist
        music_directory.mkdir(parents=True, exist_ok=True)
        logs_directory.mkdir(parents=True, exist_ok=True)
        duplicate_folders_directory.mkdir(parents=True, exist_ok=True)
        cache_directory.mkdir(parents=True, exist_ok=True)

        return music_directory, logs_directory, duplicate_folders_directory, cache_directory
    except Exception as error:
        logging.error(f'error setting up directories: {error}')
        raise


def process_artists_top_level(base_directory, duplicate_folders_directory, cache_directory):
    """
    process and merge artist directories at the top level
    """
    try:
        logging.info("processing artist directories at the top level...")

        # dictionary to map artist base names to their paths
        artist_map = {}

        # iterate only the top-level directories
        for folder_name in os.listdir(base_directory):
            folder_name = str(folder_name)  # ensure folder_name is a string
            artist_path = base_directory / folder_name

            # ensure it's a directory
            if not artist_path.is_dir():
                continue

            # extract base name (e.g., `elana_dara` from `elana_dara_copy1`)
            base_name = folder_name.split('_copy')[0]

            # group directories by base name
            artist_map.setdefault(base_name, []).append(artist_path)

        # process each group in the artist map
        for base_name, artist_group in artist_map.items():
            # Only process if there is more than one folder for the same artist
            if len(artist_group) > 1:
                # create a directory in /config/cache for the base name
                cache_folder = cache_directory / base_name
                cache_folder.mkdir(parents=True, exist_ok=True)

                # copy content of all grouped folders to the cache directory
                for folder in artist_group:
                    for item in os.listdir(folder):
                        item = str(item)  # ensure item is a string
                        source_path = folder / item
                        target_path = cache_folder / item

                        if source_path.is_dir():
                            logging.info(f"copying directory: {source_path} -> {target_path}")
                            shutil.copytree(source_path, target_path, dirs_exist_ok=True)
                        else:
                            logging.info(f"copying file: {source_path} -> {target_path}")
                            shutil.copy2(source_path, target_path)

                # move original folders to the duplicate folder directory
                for folder in artist_group:
                    target_folder = duplicate_folders_directory / folder.name

                    # check if the target directory already exists
                    if target_folder.exists():
                        logging.info(f"destination path '{target_folder}' already exists. removing and overwriting.")
                        shutil.rmtree(target_folder)

                    logging.info(f"moving original folder: {folder} -> {target_folder}")
                    shutil.move(str(folder), str(target_folder))

                # move the merged cache folder back to the original directory
                target_path = base_directory / base_name
                logging.info(f"moving merged directory: {cache_folder} -> {target_path}")
                shutil.move(str(cache_folder), str(target_path))

        logging.info("artist directory processing completed successfully.")
    except Exception as error:
        logging.error(f"error processing artist directories: {error}")
        raise


# CONFIGURE LOGGING
try:
    music_dir, logs_dir, duplicate_dir, cache_dir = setup_directories()
    log_path = logs_dir / 'artist_folders_merger.log'
    logging.basicConfig(filename=log_path, level=logging.INFO)
except Exception as e:
    print(f'[cruix-music-archiver] error setting up logging: {e}')
    raise

# NOTIFY START OF PROCESS
print("[cruix-music-archiver] starting the artist folder merging process... 🎶  💥  let the transformation begin! 🎶  💥", flush=True)

# PROCESS MUSIC DIRECTORY
try:
    process_artists_top_level(music_dir, duplicate_dir, cache_dir)  # process artist folders at the top level
except Exception as e:
    logging.error(f'error executing script: {e}')
    raise

# NOTIFY END OF PROCESS
print("[cruix-music-archiver] artist folder merged successfully... 🎉  your files are now perfectly organized and ready to shine! 🎉")