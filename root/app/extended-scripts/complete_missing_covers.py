import os
import shutil
import logging
from PIL import Image, UnidentifiedImageError
from pathlib import Path

# Absolute paths for logs and downloads directories
log_dir = Path('/config/logs')
downloads_dir = Path('/downloads')

# Ensure that the log directory exists
log_dir.mkdir(parents=True, exist_ok=True)

# Log configuration
logging.basicConfig(filename=log_dir / 'complete_missing_covers.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("COMPLETING MISSING COVERS...")

# List of audio formats supported by FFmpeg
ffmpeg_supported_audio_formats = [
    '.mp3', '.flac', '.wav', '.aac', '.m4a', '.ogg', '.wma', '.alac', '.aiff',
    '.opus', '.dsd', '.amr', '.ape', '.ac3', '.mp2', '.wv', '.m4b', '.mka',
    '.spx', '.caf', '.snd', '.gsm', '.tta', '.voc', '.w64', '.s8', '.u8'
]

def validate_directory(directory):
    if not directory.is_dir():
        logging.error(f'DIRECTORY NOT FOUND: {directory}')
        return False
    return True

def process_image(source, width, height):
    try:
        with Image.open(source) as img:
            img_width, img_height = img.size
            logging.info(f'Processing {source}: {img_width}x{img_height}')  # Log dimensions
        return img_width == width and img_height == height
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
        jpg_files = [file for file in files if file.endswith(('.jpg', '.jpeg', '.png'))]  # Added support for PNG
        audio_files = [file for file in files if any(file.endswith(ext) for ext in ffmpeg_supported_audio_formats)]

        for audio_file in audio_files:
            audio_name = Path(audio_file).stem
            if not any(jpg_file.startswith(audio_name) for jpg_file in jpg_files):
                for jpg_file in jpg_files:
                    source = Path(root) / jpg_file
                    if process_image(source, width, height):
                        destination = Path(root) / f'{audio_name}.jpg'
                        shutil.copy2(source, destination)
                        logging.info(f'FILE COPIED: {source} TO {destination}')
                        break

    logging.info('PROCESS COMPLETED.')

# Run main function
copy_first_image_to_audio(downloads_dir)

logging.info("MISSING COVERS COMPLETED.")