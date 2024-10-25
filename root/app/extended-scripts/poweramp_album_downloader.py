import os
import shutil
import logging


def setup_directories():
    """sets up the log and music directories using fixed absolute paths."""
    # defining absolute paths
    log_dir = '/config/logs'
    music_dir = '/music'

    # ensure directories exist
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(music_dir, exist_ok=True)

    return log_dir, music_dir


# call the function to set up directories
logs_directory, music_directory = setup_directories()

print("\nconfiguring poweramp album covers...")

# set up logging
log_filename = os.path.join(logs_directory, 'poweramp_album_downloader.log')
logging.basicConfig(filename=log_filename, level=logging.INFO)


def copy_first_jpg(directory):
    """copies the first .jpg file found in each directory or subdirectory."""
    try:
        # ensure directory is a string
        directory = str(directory)  # convert to string if it's not already

        for root, dirs, files in os.walk(directory):  # walk through directory and subdirectories
            for file in files:
                if file.endswith('.jpg'):
                    # ensure root and file are treated as strings
                    source = os.path.join(root, file)  # construct source path (where the file was found)
                    destination = os.path.join(root, 'albumart.jpg')  # construct destination path in same folder

                    if not os.path.exists(destination):
                        shutil.copy2(source, destination)  # copy to the same directory
                        logging.info(f'cover copied: {source} to {destination}\n')
                    else:
                        logging.info(f'cover not copied: {destination} already exists.\n')
                    break  # stops after copying the first found file in each directory
    except (FileNotFoundError, PermissionError) as e:
        logging.error(f'error copying cover: {e}\n')
    except Exception as e:
        logging.error(f'unexpected error occurred: {e}\n')


# execute the function to copy .JPG files
copy_first_jpg(music_directory)

print("poweramp album covers configured successfully.")