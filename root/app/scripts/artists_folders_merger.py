import os
import logging
import shutil
from pathlib import Path

def setup_directories():
    """
    setup directories and ensure they exist
    """
    try:
        music_directory = Path('/music').resolve()
        logs_directory = Path('/config/logs').resolve()
        duplicate_folders_directory = Path('/config/duplicated-artists-folders').resolve()
        cache_directory = Path('/config/cache').resolve()

        # ensure directories exist
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
            base_name = folder_name.split('copy')[0]

            # group directories by base name
            artist_map.setdefault(base_name, []).append(artist_path)

        # process each group in the artist map
        for base_name, artist_group in artist_map.items():
            # only process if there is more than one folder for the same artist
            if len(artist_group) > 1:
                # create a directory in /config/cache for the base name
                cache_folder = cache_directory / base_name
                cache_folder.mkdir(parents=True, exist_ok=True)

                # copy content of all grouped folders to the cache directory
                for folder in artist_group:
                    for item in folder.iterdir():
                        target_path = cache_folder / item.name

                        if item.is_dir():
                            shutil.copytree(item, target_path, dirs_exist_ok=True)
                        else:
                            shutil.copy2(item, target_path)  # Sobrescreve arquivos existentes

                # move original folders to the duplicate folder directory
                for folder in artist_group:
                    target_folder = duplicate_folders_directory / folder.name
                    target_folder.mkdir(parents=True, exist_ok=True)

                    for item in folder.iterdir():
                        target_path = target_folder / item.name
                        if item.is_dir():
                            shutil.copytree(item, target_path, dirs_exist_ok=True)
                        else:
                            shutil.copy2(item, target_path)  # Sobrescreve arquivos existentes

                    logging.info(f"[cruix-music-archiver] Deleting Original Folder: {folder}")
                    print(f"[cruix-music-archiver] Deleting Original Folder: {folder}   🗑️  ")
                    shutil.rmtree(folder)

                # move the merged cache folder back to the original directory
                target_path = base_directory / base_name
                shutil.copytree(cache_folder, target_path, dirs_exist_ok=True)
                shutil.rmtree(cache_folder)

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
    print(f'[cruix-music-archiver] Error Setting Up Logging: {e}')
    raise

# NOTIFY START OF PROCESS
print("[cruix-music-archiver] Artists Folders Merging Process...  📂  ➡️   Let the Transformation Begin!  🚀  🔄 ", flush=True)

# PROCESS MUSIC DIRECTORY
try:
    process_artists_top_level(music_dir, duplicate_dir, cache_dir)  # process artist folders at the top level
except Exception as e:
    logging.error(f'error executing script: {e}')
    raise

# NOTIFY END OF PROCESS
print("[cruix-music-archiver] Artists Folder Merged Successfully...  📂  ✅  Your Files Are Now Perfectly Organized and Ready to Shine! 🗂️  ✨ ")