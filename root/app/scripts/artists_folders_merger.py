import os
import logging
import shutil
from pathlib import Path


def setup_directories():
    """
    Setup directories and ensure they exist.
    """
    try:
        music_directory = Path('/music').resolve()
        logs_directory = Path('/config/logs').resolve()
        duplicate_folders_directory = Path('/config/duplicated-artists-folders').resolve()
        cache_directory = Path('/config/cache').resolve()
        backup_directory = Path('/config/backup').resolve()  # New backup folder

        # Ensure directories exist
        music_directory.mkdir(parents=True, exist_ok=True)
        logs_directory.mkdir(parents=True, exist_ok=True)
        duplicate_folders_directory.mkdir(parents=True, exist_ok=True)
        cache_directory.mkdir(parents=True, exist_ok=True)
        backup_directory.mkdir(parents=True, exist_ok=True)  # Ensure backup directory exists

        return music_directory, logs_directory, duplicate_folders_directory, cache_directory, backup_directory
    except Exception as error:
        logging.error(f'Error setting up directories: {error}')
        raise


def process_artists_top_level(base_directory, duplicate_folders_directory, cache_directory, backup_directory):
    """
    Process and merge artist directories at the top level.
    """
    try:
        logging.info("Processing artist directories at the top level...")

        artist_map = {}

        # Iterate over directories at the top level
        for folder_name in os.listdir(base_directory):
            folder_name = str(folder_name)
            artist_path = base_directory / folder_name

            if not artist_path.is_dir():
                continue

            # Extract base name (e.g., `elana_dara` from `elana_dara_copy1`)
            base_name = folder_name.split('copy')[0]
            artist_map.setdefault(base_name, []).append(artist_path)

        # Process each group of artist directories
        for base_name, artist_group in artist_map.items():
            if len(artist_group) > 1:
                cache_folder = cache_directory / base_name
                cache_folder.mkdir(parents=True, exist_ok=True)

                # copy content of all grouped folders to cache folder
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

                # Move original folders to the duplicate folder directory
                for folder in artist_group:
                    target_folder = duplicate_folders_directory / folder.name
                    try:
                        logging.info(f"[cruix-music-archiver] Moving Folder: {folder} to {target_folder}")
                        shutil.copytree(folder, target_folder, dirs_exist_ok=True)  # Copy to duplicate folder
                        logging.info(f"[cruix-music-archiver] Moving Folder: {folder} to Backup")
                        backup_target_folder = backup_directory / folder.name  # Backup path
                        shutil.copytree(folder, backup_target_folder, dirs_exist_ok=True)  # Move to backup

                        logging.info(f"[cruix-music-archiver] Deleting Original Folder: {folder}")
                        shutil.rmtree(folder)  # Delete after moving
                    except Exception as error:
                        logging.error(f"[cruix-music-archiver] Error Moving Folder '{folder}' to '{target_folder}': {error}")
                        raise

                # Move merged cache folder back to the original directory
                target_path = base_directory / base_name
                try:
                    logging.info(f"[cruix-music-archiver] Copying Merged Directory: {cache_folder} to {target_path}")
                    shutil.copytree(cache_folder, target_path, dirs_exist_ok=True)
                    logging.info(f"[cruix-music-archiver] Deleting Cache Folder: {cache_folder}")
                    shutil.rmtree(cache_folder)
                except Exception as error:
                    logging.error(f"[cruix-music-archiver] Error Moving Merged Folder '{cache_folder}' to '{target_path}': {error}")
                    raise

        logging.info("Artist directory processing completed successfully.")
    except Exception as error:
        logging.error(f"Error processing artist directories: {error}")
        raise


# CONFIGURE LOGGING
try:
    music_dir, logs_dir, duplicate_dir, cache_dir, backup_dir = setup_directories()
    log_path = logs_dir / 'artist_folders_merger.log'
    logging.basicConfig(filename=log_path, level=logging.INFO)
except Exception as e:
    print(f'[cruix-music-archiver] Error Setting Up Logging: {e}')
    raise

# NOTIFY START OF PROCESS
print("[cruix-music-archiver] Artists Folders Merging Process...  📂  ➡️   Let the Transformation Begin!  🚀  🔄 ", flush=True)

# PROCESS MUSIC DIRECTORY
try:
    process_artists_top_level(music_dir, duplicate_dir, cache_dir, backup_dir)
except Exception as e:
    logging.error(f'Error executing script: {e}')
    raise

# NOTIFY END OF PROCESS
print("[cruix-music-archiver] Artists Folder Merged Successfully...  📂  ✅  Your Files Are Now Perfectly Organized and Ready to Shine! 🗂️  ✨ ")