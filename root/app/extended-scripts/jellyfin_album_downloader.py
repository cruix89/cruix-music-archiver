import os
import shutil
import logging


def setup_directories():
    """Sets up the log and music directories using fixed absolute paths."""
    # DEFINING ABSOLUTE PATHS
    log_dir = '/config/logs'
    music_dir = '/downloads'

    # ENSURE DIRECTORIES EXIST
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(music_dir, exist_ok=True)

    return log_dir, music_dir


# CALL THE FUNCTION TO SET UP DIRECTORIES
logs_directory, music_directory = setup_directories()

print("\nconfiguring album covers...")

# SET UP LOGGING
log_filename = os.path.join(logs_directory, 'jellyfin_album_downloader.log')
logging.basicConfig(filename=log_filename, level=logging.INFO)


def copy_first_jpg(directory):
    """Copies the first .jpg file found in each directory or subdirectory."""
    try:
        # Ensure directory is a string
        directory = str(directory)  # Convert to string if it's not already

        for root, dirs, files in os.walk(directory):  # Walk through directory and subdirectories
            for file in files:
                if file.endswith('.jpg'):
                    # Ensure root and file are treated as strings
                    source = os.path.join(root, file)  # Construct source path (where the file was found)
                    destination = os.path.join(root, 'folder.jpg')  # Construct destination path in same folder

                    if not os.path.exists(destination):
                        shutil.copy2(source, destination)  # Copy to the same directory
                        logging.info(f'cover copied: {source} to {destination}\n')
                    else:
                        logging.info(f'cover not copied: {destination} already exists.\n')
                    break  # Stops after copying the first found file in each directory
    except (FileNotFoundError, PermissionError) as e:
        logging.error(f'error copying cover: {e}\n')
    except Exception as e:
        logging.error(f'unexpected error occurred: {e}\n')


# EXECUTE THE FUNCTION TO COPY .JPG FILES
copy_first_jpg(music_directory)

print("album covers configured successfully.")