import os
import shutil
import logging
from PIL import Image, UnidentifiedImageError

# ABSOLUTE PATHS FOR LOGS AND DOWNLOADS DIRECTORIES
log_dir = str('/config/logs')
downloads_dir = str('/downloads')

# ENSURE THAT THE LOG DIRECTORY EXISTS
os.makedirs(log_dir, exist_ok=True)

# LOG CONFIGURATION
logging.basicConfig(filename=os.path.join(str(log_dir), 'complete_missing_covers.log'), level=logging.INFO)

print("COMPLETING MISSING COVERS...")

# LIST OF AUDIO FORMATS SUPPORTED BY FFMPEG
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


def process_image(source, width, height):
    try:
        with Image.open(source) as img:
            img_width, img_height = img.size
        if img_width == width and img_height == height:
            return True
    except UnidentifiedImageError:
        logging.error(f'ERROR IDENTIFYING IMAGE: {source}')
    except Exception as e:
        logging.error(f'ERROR PROCESSING FILE {source}: {e}')
    return False


def copy_first_image_to_audio(directory, width=544, height=544):
    if not validate_directory(directory):
        return

    logging.info(f'STARTING PROCESS IN DIRECTORY: {directory}')
    for root, _, files in os.walk(directory):
        jpg_files = [file for file in files if file.endswith('.jpg')]
        audio_files = [file for file in files if any(file.endswith(ext) for ext in ffmpeg_supported_audio_formats)]

        for audio_file in audio_files:
            audio_name = os.path.splitext(audio_file)[0]
            if not any(jpg_file.startswith(audio_name) for jpg_file in jpg_files):
                for jpg_file in jpg_files:
                    source = os.path.join(str(root), str(jpg_file))
                    if process_image(source, width, height):
                        destination = os.path.join(str(root), f'{str(audio_name)}.jpg')
                        shutil.copy2(source, destination)
                        logging.info(f'FILE COPIED: {source} TO {destination}')
                        break

    logging.info('PROCESS COMPLETED.')


# RUN MAIN FUNCTION
copy_first_image_to_audio(downloads_dir)

print("MISSING COVERS COMPLETED.")