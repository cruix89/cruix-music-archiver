import os
import logging

# absolute paths for logs and downloads directories
log_dir = '/config/logs'
downloads_dir = '/downloads'

# ensure that the log directory exists
os.makedirs(log_dir, exist_ok=True)

# log configuration
logging.basicConfig(filename=os.path.join(log_dir, 'complete_missing_covers.log'),
                    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print("\nCOMPLETING MISSING COVERS...")
logging.info("COMPLETING MISSING COVERS...")

# list of audio formats supported by FFMPEG
ffmpeg_supported_audio_formats = [
    '.mp3', '.flac', '.wav', '.aac', '.m4a', '.ogg', '.wma', '.alac', '.aiff',
    '.opus', '.dsd', '.amr', '.ape', '.ac3', '.mp2', '.wv', '.m4b', '.mka',
    '.spx', '.caf', '.snd', '.gsm', '.tta', '.voc', '.w64', '.s8', '.u8'
]

def validate_directory(directory):
    if not os.path.isdir(directory):
        logging.error(f'DIRECTORY NOT FOUND: {directory}')
        return False
    return True

def find_first_image(files):
    """find the first image in the directory."""
    for file in files:
        # Check if the file is an image
        if file.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            logging.info(f'First image found: {file}')
            return file
    return None

def copy_file(source, destination):
    """copy a file from source to destination."""
    with open(source, 'rb') as src_file:
        with open(destination, 'wb') as dst_file:
            dst_file.write(src_file.read())
    logging.info(f'FILE COPIED: {source} TO {destination}')

def copy_first_image_to_audio(directory):
    if not validate_directory(directory):
        return

    logging.info(f'STARTING PROCESS IN DIRECTORY: {directory}')
    for root, _, files in os.walk(directory):
        jpg_files = [file for file in files if file.endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        audio_files = [file for file in files if any(file.endswith(ext) for ext in ffmpeg_supported_audio_formats)]

        if not jpg_files:
            logging.warning(f'NO IMAGES FOUND IN: {root}')
            continue

        # find the first image in the directory
        first_image = find_first_image(jpg_files)

        if first_image:
            for audio_file in audio_files:
                audio_name = os.path.splitext(audio_file)[0]
                if not any(jpg_file.startswith(audio_name) for jpg_file in jpg_files):
                    source = os.path.join(root, first_image)
                    destination = os.path.join(root, f'{audio_name}.jpg')
                    try:
                        copy_file(source, destination)
                    except Exception as e:
                        logging.error(f'ERROR COPYING FILE: {source} TO {destination} - {e}')
        else:
            logging.warning(f'NO SUITABLE IMAGE FOUND IN: {root}')

    logging.info('PROCESS COMPLETED.')

# run main function
copy_first_image_to_audio(downloads_dir)

print("MISSING COVERS COMPLETED.")
logging.info("MISSING COVERS COMPLETED.")