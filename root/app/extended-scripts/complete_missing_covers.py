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

def calculate_size_difference(image_size, target_size=(544, 544)):
    """Calculates the difference between the image size and the target size."""
    width_diff = abs(image_size[0] - target_size[0])
    height_diff = abs(image_size[1] - target_size[1])
    return width_diff + height_diff  # Total difference in width and height

def find_best_image(files, root, target_size=(544, 544)):
    """Find the image with the smallest size difference from the target size."""
    closest_image = None
    smallest_difference = float('inf')

    for file in files:
        try:
            with Image.open(Path(root) / file) as img:
                size_difference = calculate_size_difference(img.size, target_size)
                logging.info(f'Processing {file}: {img.size} (difference: {size_difference})')

                if size_difference < smallest_difference:
                    smallest_difference = size_difference
                    closest_image = file

        except UnidentifiedImageError:
            logging.error(f'ERROR IDENTIFYING IMAGE: {file}')
        except Exception as e:
            logging.error(f'ERROR PROCESSING FILE {file}: {e}')

    return closest_image

def copy_best_image_to_audio(directory, target_size=(544, 544)):
    if not validate_directory(directory):
        return

    logging.info(f'STARTING PROCESS IN DIRECTORY: {directory}')
    for root, _, files in os.walk(directory):
        # Added support for WebP images
        jpg_files = [file for file in files if file.endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        audio_files = [file for file in files if any(file.endswith(ext) for ext in ffmpeg_supported_audio_formats)]

        for audio_file in audio_files:
            audio_name = Path(audio_file).stem
            if not any(jpg_file.startswith(audio_name) for jpg_file in jpg_files):  # Ignore the name matching
                best_image = find_best_image(jpg_files, root, target_size)
                if best_image:
                    source = Path(root) / best_image
                    destination = Path(root) / f'{audio_name}.jpg'  # Still saving as .jpg
                    shutil.copy2(source, destination)
                    logging.info(f'FILE COPIED: {source} TO {destination}')
                else:
                    logging.warning(f'NO SUITABLE IMAGE FOUND FOR: {audio_file}')

    logging.info('PROCESS COMPLETED.')

# Run main function
copy_best_image_to_audio(downloads_dir)

logging.info("MISSING COVERS COMPLETED.")