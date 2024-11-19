import os
import logging
import shutil


def setup_directories():
    try:
        music_directory = '/music'
        logs_directory = '/config/logs'
        cache_directory = '/config/cache'
        return music_directory, logs_directory, cache_directory
    except Exception as error:
        logging.error(f'error setting up directories: {error}')
        raise


def merge_folders_with_cache(base_directory, cache_directory='/config/cache'):
    try:
        logging.info("merging duplicate folders using cache...")

        # dictionary to map folders with the same base name without the '_copy' suffix
        folder_map = {}

        # identifying duplicate folders
        for root, dirs, _ in os.walk(base_directory, topdown=False):
            for folder_name in dirs:
                base_name = folder_name.split('_copy')[0]  # remove the '_copy' suffix for comparison
                folder_map.setdefault((root, base_name), []).append(os.path.join(root, folder_name))

        # process each group of duplicate folders
        for (root, base_name), folder_group in folder_map.items():
            if len(folder_group) > 1:
                # unique directory in the cache
                target_cache_folder = os.path.join(cache_directory, base_name)

                if not os.path.exists(target_cache_folder):
                    os.makedirs(target_cache_folder)

                # move the contents of all duplicate folders to the cache
                for folder_path in folder_group:
                    for item in os.listdir(folder_path):
                        source_path = os.path.join(folder_path, item)
                        target_path = os.path.join(target_cache_folder, item)

                        # handle conflicts (replace files or merge folders)
                        if os.path.exists(target_path):
                            if os.path.isfile(source_path):
                                os.remove(target_path)
                                shutil.move(source_path, target_path)
                        else:
                            shutil.move(source_path, target_path)

                    # remove the original directory after moving its contents
                    os.rmdir(folder_path)

                # determine the final path in the base directory
                final_target_folder = os.path.join(root, base_name)

                # if it already exists, remove it before moving the cache
                if os.path.exists(final_target_folder):
                    shutil.rmtree(final_target_folder)
                shutil.move(target_cache_folder, final_target_folder)

        logging.info("duplicate folders merged successfully using cache.")
    except Exception as error:
        logging.error(f"error merging folders using cache: {error}")
        raise


# CONFIGURE LOGGING
try:
    music_dir, logs_dir, cache_dir = setup_directories()
    log_path = os.path.join(logs_dir, 'folders_merger.log')
    logging.basicConfig(filename=log_path, level=logging.INFO)
except Exception as e:
    print(f'[cruix-music-archiver] error setting up logging: {e}')
    raise

# NOTIFY START OF PROCESS
print("[cruix-music-archiver] starting the folder merging process... 🎶  💥  let the transformation begin!")

# PROCESS MUSIC DIRECTORY
try:
    merge_folders_with_cache(music_dir, cache_dir)  # merge folders using cache
except Exception as e:
    logging.error(f'error executing script: {e}')
    raise

# NOTIFY END OF PROCESS
print("[cruix-music-archiver] folder merging process completed successfully... 🎉  your files are now perfectly organized and ready to shine!")