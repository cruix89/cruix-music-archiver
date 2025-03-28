import os
import logging
import shutil
from pathlib import Path
from datetime import datetime
import time


def handle_remove_error(func, path, exc_info):
    """
    handles errors during directory removal by waiting for a brief interval and retrying multiple times.

    the parameter `exc_info` is logged to provide details about the original exception.
    """
    max_attempts = 5  # maximum number of removal attempts
    attempt = 0

    # log the original error information from exc_info once
    logging.error(f"Initial error removing {path}. Exception info: {exc_info}")

    while attempt < max_attempts:
        time.sleep(5)  # wait for 5 seconds between attempts
        # if the directory exists, attempt to remove any residual content
        if os.path.isdir(path):
            try:
                for entry in os.listdir(path):
                    full_entry = os.path.join(path, entry)
                    if os.path.isdir(full_entry):
                        shutil.rmtree(full_entry, ignore_errors=True)
                    else:
                        os.remove(full_entry)
            except Exception as cleanup_error:
                logging.error(f"error cleaning directory {path}: {cleanup_error}")

        try:
            func(path)
            return  # exit the function if removal is successful
        except Exception as remove_error:
            attempt += 1
            logging.error(f"attempt {attempt} failed to remove {path}: {remove_error}", exc_info=exc_info)

    # if maximum attempts are exceeded, raise an exception
    raise Exception(f"failed to remove directory {path} after {max_attempts} attempts")


def setup_directories():
    """
    sets up directories and ensures they exist.
    """
    try:
        music_directory = Path('/music').resolve()
        logs_directory = Path('/config/logs').resolve()
        cache_directory = Path('/config/cache').resolve()
        backup_directory = Path('/config/merged-folders-backup').resolve()

        # ensure directories exist
        music_directory.mkdir(parents=True, exist_ok=True)
        logs_directory.mkdir(parents=True, exist_ok=True)
        cache_directory.mkdir(parents=True, exist_ok=True)
        backup_directory.mkdir(parents=True, exist_ok=True)

        return music_directory, logs_directory, cache_directory, backup_directory
    except Exception as setup_error:
        logging.error(f'error setting up directories: {setup_error}')
        raise


def process_artists_top_level(base_directory, cache_directory, backup_directory):
    """
    processes and merges artist directories at the top level.
    """
    try:
        logging.info("processing artist directories at the top level...")

        artist_map = {}

        # iterate over directories at the top level
        for folder_name in os.listdir(base_directory):
            folder_name = str(folder_name)
            artist_path = base_directory / folder_name

            if not artist_path.is_dir():
                continue

            # extract base name
            base_name = folder_name.split('copy')[0]
            artist_map.setdefault(base_name, []).append(artist_path)

        # process each group of artist directories
        for base_name, artist_group in artist_map.items():
            if len(artist_group) > 1:
                cache_folder = cache_directory / base_name
                cache_folder.mkdir(parents=True, exist_ok=True)

                # backup the original folders before any modifications
                for folder in artist_group:
                    try:
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        backup_target_folder = backup_directory / f"{folder.name}_{timestamp}"

                        logging.info(f"[cruix-music-archiver] Creating Backup for Folder: {folder}  📚")
                        shutil.copytree(folder, backup_target_folder, dirs_exist_ok=True)
                    except Exception as backup_error:
                        logging.error(
                            f"[cruix-music-archiver] Error Creating Backup for Folder '{folder}': {backup_error}")
                        raise

                # copy contents of all grouped folders to the cache folder
                for folder in artist_group:
                    for item in os.listdir(folder):
                        item = str(item)
                        source_path = folder / item
                        target_path = cache_folder / item

                        if source_path.is_dir():
                            logging.info(f"[cruix-music-archiver] Copying Directory: {source_path} to {target_path}")
                            shutil.copytree(source_path, target_path, dirs_exist_ok=True)
                        else:
                            logging.info(f"[cruix-music-archiver] Copying File: {source_path} to {target_path}")
                            shutil.copy2(source_path, target_path)

                # delete original folders after creating the backup
                for folder in artist_group:
                    try:
                        logging.info(f"[cruix-music-archiver] Deleting Original Folder: {folder}")
                        shutil.rmtree(folder, ignore_errors=True)
                    except Exception as delete_error:
                        logging.error(f"[cruix-music-archiver] Error Deleting Folder '{folder}': {delete_error}")
                        raise

                # move the merged cache folder back to the original directory
                target_path = base_directory / base_name
                try:
                    logging.info(f"[cruix-music-archiver] Copying Merged Directory: {cache_folder} to {target_path}")
                    shutil.copytree(cache_folder, target_path, dirs_exist_ok=True)
                    logging.info(f"[cruix-music-archiver] Deleting Cache Folder: {cache_folder}")
                    shutil.rmtree(cache_folder, ignore_errors=True)
                except Exception as move_error:
                    logging.error(
                        f"[cruix-music-archiver] Error Moving Merged Folder '{cache_folder}' to '{target_path}': {move_error}")
                    raise

        logging.info("artist directory processing completed successfully.")
    except Exception as processing_error:
        logging.error(f"error processing artist directories: {processing_error}")
        raise


# CONFIGURE LOGGING
try:
    music_dir, logs_dir, cache_dir, backup_dir = setup_directories()
    log_path = logs_dir / 'artist_folders_merger.log'
    logging.basicConfig(filename=log_path, level=logging.INFO)
except Exception as logging_error:
    print(f'[cruix-music-archiver] Error Setting Up Logging: {logging_error}')
    raise

# NOTIFY START OF PROCESS
print("[cruix-music-archiver] Artists Folders Merging Process...  📚  ➡️   Let the Transformation Begin!  🚀  🛠 ",
      flush=True)

# PROCESS MUSIC DIRECTORY
try:
    process_artists_top_level(music_dir, cache_dir, backup_dir)
except Exception as execution_error:
    logging.error(f'error executing script: {execution_error}')
    raise

# NOTIFY END OF PROCESS
print(
    "[cruix-music-archiver] Artists Folder Merged Successfully...  📚  ✅  Your Files Are Now Perfectly Organized and Ready to Shine! 🗂  ✨ ")